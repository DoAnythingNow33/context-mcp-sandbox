// GitHub backend for a context vault. The client's repo is the vault: we list, read, search and
// commit through the GitHub REST API. No clone, no git binary, and nothing is stored on our side
// (compliance rule 1) — search pulls the repo tarball into memory and discards it.

export const TEXT_SUFFIXES = [".md", ".txt", ".yaml", ".yml", ".json", ".csv", ".base", ".html"];
const MAX_TEXT_BYTES = 1_000_000; // skip anything larger when searching; vault notes are small

export const isText = (path: string) => TEXT_SUFFIXES.some((s) => path.toLowerCase().endsWith(s));

export interface Author {
  name: string;
  email: string;
}

export interface RepoRef {
  owner: string;
  repo: string;
  branch: string;
  /** Returns a token for this repo: a PAT in tests, a GitHub App installation token in production. */
  token: () => Promise<string>;
  fetch?: typeof fetch;
  apiBase?: string;
}

export class GitHubError extends Error {
  constructor(message: string, readonly status: number) {
    super(message);
  }
}

/** Thrown by a write transform to abort the write with a message for the agent. */
export class WriteRefused extends Error {}

const MAX_WRITE_ATTEMPTS = 4;

export class GitHubVault {
  private readonly fetch: typeof fetch;
  private readonly api: string;

  constructor(private readonly ref: RepoRef) {
    this.fetch = ref.fetch ?? fetch.bind(globalThis);
    this.api = `${ref.apiBase ?? "https://api.github.com"}/repos/${ref.owner}/${ref.repo}`;
  }

  private async request(path: string, init: RequestInit = {}, accept = "application/vnd.github+json") {
    const res = await this.fetch(this.api + path, {
      ...init,
      headers: {
        accept,
        authorization: `Bearer ${await this.ref.token()}`,
        "x-github-api-version": "2022-11-28",
        "user-agent": "context-mcp",
        ...(init.body ? { "content-type": "application/json" } : {}),
      },
    });
    return res;
  }

  private async fail(res: Response, what: string): Promise<never> {
    const body = await res.text().catch(() => "");
    let detail = body.slice(0, 200);
    try {
      detail = JSON.parse(body).message ?? detail;
    } catch {}
    throw new GitHubError(`GitHub ${what}: ${res.status} ${detail}`, res.status);
  }

  /** Every text file path in the branch (one API call). */
  async listFiles(): Promise<string[]> {
    const res = await this.request(`/git/trees/${encodeURIComponent(this.ref.branch)}?recursive=1`);
    if (!res.ok) await this.fail(res, "list");
    const data = (await res.json()) as { tree: { path: string; type: string }[]; truncated: boolean };
    if (data.truncated) throw new GitHubError("GitHub list: repo tree too large (truncated)", 413);
    return data.tree.filter((e) => e.type === "blob" && isText(e.path)).map((e) => e.path).sort();
  }

  /** File text plus its blob sha, or null if it doesn't exist. */
  async readFile(path: string): Promise<{ text: string; sha: string } | null> {
    const res = await this.request(`/contents/${encodePath(path)}?ref=${encodeURIComponent(this.ref.branch)}`);
    if (res.status === 404) return null;
    if (!res.ok) await this.fail(res, `read ${path}`);
    const data = (await res.json()) as { type: string; sha: string; content?: string; encoding?: string };
    if (data.type !== "file") return null;
    if (data.encoding === "base64" && data.content !== undefined)
      return { text: fromBase64(data.content), sha: data.sha };
    // Files over 1 MB come back without content; fall back to the blob API.
    const blob = await this.request(`/git/blobs/${data.sha}`, {}, "application/vnd.github.raw");
    if (!blob.ok) await this.fail(blob, `read ${path}`);
    return { text: await blob.text(), sha: data.sha };
  }

  /** All text files in the branch, read from one tarball download, held in memory only. */
  async snapshot(): Promise<Map<string, string>> {
    const res = await this.request(`/tarball/${encodeURIComponent(this.ref.branch)}`);
    if (!res.ok || !res.body) await this.fail(res, "tarball");
    const tar = new Uint8Array(await new Response(res.body!.pipeThrough(new DecompressionStream("gzip"))).arrayBuffer());
    const files = new Map<string, string>();
    const decoder = new TextDecoder();
    for (const { path, data } of readTar(tar)) {
      // Entries are prefixed "<owner>-<repo>-<sha>/".
      const rel = path.slice(path.indexOf("/") + 1);
      if (rel && isText(rel) && data.length <= MAX_TEXT_BYTES) files.set(rel, decoder.decode(data));
    }
    return files;
  }

  /**
   * Commit one file straight to the branch, authored as `author`. `transform` gets the current text
   * (null if the file doesn't exist) and returns the new text, or throws WriteRefused. On a sha
   * conflict (someone else committed in between) it re-reads and re-applies, so additive writes
   * never clobber each other.
   */
  async writeFile(
    path: string,
    transform: (current: string | null) => string,
    message: string,
    author: Author,
  ): Promise<{ commit: string }> {
    for (let attempt = 1; ; attempt++) {
      const current = await this.readFile(path);
      const text = transform(current?.text ?? null);
      const res = await this.request(`/contents/${encodePath(path)}`, {
        method: "PUT",
        body: JSON.stringify({
          message,
          content: toBase64(text),
          branch: this.ref.branch,
          author,
          ...(current ? { sha: current.sha } : {}),
        }),
      });
      if (res.ok) {
        const data = (await res.json()) as { commit: { sha: string } };
        return { commit: data.commit.sha };
      }
      // 409 = sha moved; 422 = file appeared since we read it (no sha supplied).
      const raced = res.status === 409 || (res.status === 422 && !current);
      if (!raced || attempt >= MAX_WRITE_ATTEMPTS) await this.fail(res, `write ${path}`);
      await new Promise((r) => setTimeout(r, 100 * 2 ** attempt));
    }
  }
}

const encodePath = (path: string) => path.split("/").map(encodeURIComponent).join("/");

function toBase64(text: string): string {
  const bytes = new TextEncoder().encode(text);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}

function fromBase64(b64: string): string {
  const bin = atob(b64.replace(/\s/g, ""));
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}

// ---------------------------------------------------------------- tar

/** Regular files from a ustar/pax archive (the format GitHub tarballs use). */
export function* readTar(buf: Uint8Array): Generator<{ path: string; data: Uint8Array }> {
  const dec = new TextDecoder();
  const str = (o: number, n: number) => {
    const b = buf.subarray(o, o + n);
    const z = b.indexOf(0);
    return dec.decode(z === -1 ? b : b.subarray(0, z));
  };
  let longPath: string | undefined;
  for (let off = 0; off + 512 <= buf.length; ) {
    if (buf[off] === 0) break; // end-of-archive block
    const size = parseInt(str(off + 124, 12).trim() || "0", 8);
    const type = String.fromCharCode(buf[off + 156] || 48); // NUL means a regular file
    const prefix = str(off + 345, 155);
    const name = str(off, 100);
    const data = buf.subarray(off + 512, off + 512 + size);
    off += 512 + Math.ceil(size / 512) * 512;
    if (type === "x") longPath = paxPath(dec.decode(data)) ?? longPath;
    else if (type === "L") longPath = dec.decode(data).replace(/\0+$/, "");
    else if (type === "0" || type === "7") {
      yield { path: longPath ?? (prefix ? `${prefix}/${name}` : name), data };
      longPath = undefined;
    } else if (type !== "g") longPath = undefined;
  }
}

// pax records: "<len> <key>=<value>\n"
function paxPath(records: string): string | undefined {
  for (const line of records.split("\n")) {
    const m = /^\d+ path=(.*)$/s.exec(line);
    if (m) return m[1];
  }
  return undefined;
}
