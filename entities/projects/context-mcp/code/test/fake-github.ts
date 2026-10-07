// In-memory stand-in for the slice of the GitHub REST API the backend uses. Behaves like the real
// thing where it matters: sha-checked writes (409 on a stale sha, 422 on create-over-existing),
// a gzipped pax tarball with a "<owner>-<repo>-<sha>/" prefix, and 404s for missing files.

const enc = new TextEncoder();

export interface Commit {
  path: string;
  message: string;
  author: { name: string; email: string };
}

export class FakeGitHub {
  files = new Map<string, string>();
  commits: Commit[] = [];
  requests: string[] = [];
  /** Runs before each PUT is applied: lets a test simulate someone else committing first. */
  beforePut?: (path: string) => void;
  private shaCounter = 0;
  private shas = new Map<string, string>();

  constructor(files: Record<string, string>, readonly token = "test-token") {
    for (const [p, t] of Object.entries(files)) this.set(p, t);
  }

  set(path: string, text: string) {
    this.files.set(path, text);
    this.shas.set(path, `sha${++this.shaCounter}`);
  }

  fetch = async (input: RequestInfo | URL, init: RequestInit = {}): Promise<Response> => {
    const url = new URL(String(input));
    const method = init.method ?? "GET";
    this.requests.push(`${method} ${url.pathname}`);
    const headers = new Headers(init.headers);
    if (headers.get("authorization") !== `Bearer ${this.token}`) return json({ message: "Bad credentials" }, 401);
    const m = /^\/repos\/acme\/vault\/(.+)$/.exec(url.pathname);
    if (!m) return json({ message: "Not Found" }, 404);
    const route = m[1];

    if (route.startsWith("git/trees/")) {
      const tree = [...this.files.keys()].map((path) => ({ path, type: "blob" }));
      const dirs = new Set([...this.files.keys()].flatMap((p) => p.split("/").slice(0, -1).map((_, i, a) => a.slice(0, i + 1).join("/"))));
      return json({ tree: [...tree, ...[...dirs].map((path) => ({ path, type: "tree" }))], truncated: false });
    }
    if (route.startsWith("git/blobs/")) {
      const sha = route.slice("git/blobs/".length);
      const path = [...this.shas].find(([, s]) => s === sha)?.[0];
      return path ? new Response(this.files.get(path)) : json({ message: "Not Found" }, 404);
    }
    if (route.startsWith("tarball/")) return new Response(await tarGz(this.files));
    if (route.startsWith("contents/")) {
      const path = decodeURIComponent(route.slice("contents/".length));
      if (method === "GET") {
        const text = this.files.get(path);
        if (text === undefined) return json({ message: "Not Found" }, 404);
        return json({ type: "file", sha: this.shas.get(path), encoding: "base64", content: b64(text) });
      }
      if (method === "PUT") {
        this.beforePut?.(path);
        const body = JSON.parse(String(init.body));
        const existing = this.shas.get(path);
        if (existing && !body.sha) return json({ message: '"sha" wasn\'t supplied.' }, 422);
        if (body.sha && body.sha !== existing) return json({ message: `${path} does not match ${body.sha}` }, 409);
        this.set(path, new TextDecoder().decode(Uint8Array.from(atob(body.content), (c) => c.charCodeAt(0))));
        this.commits.push({ path, message: body.message, author: body.author });
        return json({ commit: { sha: `commit${this.commits.length}` } }, existing ? 200 : 201);
      }
    }
    return json({ message: "Not Found" }, 404);
  };
}

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });

const b64 = (text: string) => btoa(String.fromCharCode(...enc.encode(text)));

// ---------------------------------------------------------------- tar writer

function header(name: string, size: number, type: string): Uint8Array {
  const h = new Uint8Array(512);
  const put = (s: string, off: number) => h.set(enc.encode(s), off);
  put(name.slice(0, 99), 0);
  put("0000644\0", 100);
  put(size.toString(8).padStart(11, "0") + "\0", 124);
  put(type, 156);
  put("ustar\0" + "00", 257);
  put("        ", 148);
  const sum = h.reduce((a, b) => a + b, 0);
  put(sum.toString(8).padStart(6, "0") + "\0 ", 148);
  return h;
}

function entry(name: string, data: Uint8Array, type = "0"): Uint8Array[] {
  const pad = new Uint8Array((512 - (data.length % 512)) % 512);
  return [header(name, data.length, type), data, pad];
}

function pax(key: string, value: string): Uint8Array {
  const rec = ` ${key}=${value}\n`;
  let len = rec.length + 1;
  while (String(len).length + rec.length !== len) len = String(len).length + rec.length;
  return enc.encode(len + rec);
}

/** A tarball shaped like GitHub's: global pax header, prefix dir, pax long names. */
export async function tarGz(files: Map<string, string>): Promise<Uint8Array<ArrayBuffer>> {
  const prefix = "acme-vault-abc1234/";
  const parts: Uint8Array[] = [...entry("pax_global_header", pax("comment", "abc1234"), "g"), ...entry(prefix, new Uint8Array(), "5")];
  for (const [path, text] of files) {
    const full = prefix + path;
    if (full.length > 99) parts.push(...entry("PaxHeader", pax("path", full), "x"));
    parts.push(...entry(full, enc.encode(text)));
  }
  parts.push(new Uint8Array(1024));
  const tar = new Blob(parts as BlobPart[]);
  return new Uint8Array(await new Response(tar.stream().pipeThrough(new CompressionStream("gzip"))).arrayBuffer());
}
