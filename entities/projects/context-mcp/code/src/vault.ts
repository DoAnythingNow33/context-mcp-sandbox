// The vault's tools, independent of transport. Same behaviour as v1 (context_mcp/server.py):
// get_map first, "not found" for hidden files, additive-only writes with an attribution comment,
// every write a commit authored by the member. Errors meant for the agent are AccessErrors.

import { AccessError, canRead, canWrite, normalizePath, requireLevel, visibleFiles, type Member } from "./access";
import { WriteRefused, type Author } from "./github";

export interface Tenant {
  id: string;
  plan: string;
  name: string;
  /** The vault's own entry point. A request on any other host never reaches this tenant. */
  hostname: string;
  repo: { owner: string; repo: string; branch: string };
  mapFile: string;
  orientationFiles: string[];
  flagsFile: string;
  promptDirs: string[];
  members: Member[];
}

/** What the tools need from storage; GitHubVault implements it. */
export interface Backend {
  listFiles(): Promise<string[]>;
  readFile(path: string): Promise<{ text: string } | null>;
  snapshot(): Promise<Map<string, string>>;
  writeFile(path: string, transform: (current: string | null) => string, message: string, author: Author): Promise<unknown>;
}

/** Audit rows are who/tool/path/time only, never content (compliance rule 2). */
export interface AuditEvent {
  ts: string;
  tenant: string;
  member: string;
  tool: string;
  path?: string;
}
export type Audit = (e: AuditEvent) => void;

export interface Prompt {
  name: string;
  description: string;
  path: string;
}

const LEVEL_NOTE: Record<Member["write"], string> = {
  none: "(read only).",
  flag: "(you can propose changes with raise_flag; a founder confirms them).",
  append: "(you can append to existing files and raise flags).",
  create: "(you can append, create new files and raise flags).",
};

const PROMPT_NOTE =
  "\n\n---\nYou are running this workflow through the context MCP server. Read files with " +
  "get_map / search / read_file and write only with append_to_file / create_file / raise_flag. " +
  "Skip steps that run scripts, git, or sub-agents; do their work inline or note it for the vault owner.";

export const today = () => new Date().toISOString().slice(0, 10);
const mdCell = (s: string) => s.replaceAll("|", "\\|").replaceAll("\n", " ").trim();
const stem = (p: string) => (p.split("/").pop() ?? "").replace(/\.[^.]*$/, "").toLowerCase();

/** Split YAML frontmatter off a markdown file; returns the description field if present. */
export function splitFrontmatter(text: string): { description?: string; body: string } {
  if (!text.startsWith("---\n")) return { body: text };
  const end = text.indexOf("\n---", 4);
  if (end === -1) return { body: text };
  const m = /^description:\s*(.+)$/m.exec(text.slice(4, end));
  const description = m?.[1].trim().replace(/^(["'])(.*)\1$/, "$2");
  return { description, body: text.slice(end + 4).replace(/^\n+/, "") };
}

export class VaultService {
  private files?: Promise<string[]>;

  constructor(
    private readonly tenant: Tenant,
    private readonly member: Member,
    private readonly backend: Backend,
    private readonly audit: Audit,
  ) {}

  private log(tool: string, path?: string) {
    this.audit({ ts: new Date().toISOString(), tenant: this.tenant.id, member: this.member.email, tool, ...(path ? { path } : {}) });
  }

  // One tree listing per request is plenty: a request is a single tool call.
  private allFiles() {
    return (this.files ??= this.backend.listFiles());
  }

  private get author(): Author {
    return { name: this.member.name, email: this.member.email };
  }

  private commitMessage(subject: string) {
    return `${subject}\n\nvia context-mcp (${this.member.email})`;
  }

  async getMap(): Promise<string> {
    this.log("get_map");
    const m = this.member;
    const parts = [
      `# You are connected to the '${this.tenant.name}' vault as ${m.name}`,
      `Write access: **${m.write}** ${LEVEL_NOTE[m.write]}`,
      "Some files may be hidden from you; if the map names a file you cannot read, it is out of your scope.",
      "Skills in the map that say to run scripts or git commands don't apply here: the server commits for you.",
    ];
    const wanted = [this.tenant.mapFile, ...this.tenant.orientationFiles].filter((p) => canRead(m, p));
    const texts = await Promise.all(wanted.map((p) => this.backend.readFile(p)));
    wanted.forEach((p, i) => {
      if (texts[i]) parts.push(`\n---\n# FILE: ${p}\n\n${texts[i]!.text}`);
    });
    return parts.join("\n");
  }

  async listFiles(folder = ""): Promise<string> {
    const files = visibleFiles(this.member, await this.allFiles(), folder);
    this.log("list_files", folder || undefined);
    return files.length ? `${files.length} files:\n${files.join("\n")}` : `No readable files under '${folder || "/"}'.`;
  }

  async readFile(path: string, startLine = 1, maxLines = 400): Promise<string> {
    const rel = normalizePath(path);
    this.log("read_file", rel);
    // Same message for missing and forbidden, so hidden files aren't confirmed to exist.
    const missing = `${rel}: not found or not accessible.`;
    if (!canRead(this.member, rel)) return missing;
    const file = await this.backend.readFile(rel);
    if (!file) {
      const guesses = visibleFiles(this.member, await this.allFiles()).filter((f) => stem(f) === stem(rel));
      return missing + (guesses.length ? ` Did you mean: ${guesses.join(", ")}` : "");
    }
    const lines = file.text.split("\n");
    if (lines.at(-1) === "") lines.pop();
    const start = Math.max(startLine, 1);
    const chunk = lines.slice(start - 1, start - 1 + maxLines);
    const end = start - 1 + chunk.length;
    const more = end < lines.length ? `\n\n[... ${lines.length - end} more lines: call read_file with start_line=${end + 1}]` : "";
    return `# ${rel} (lines ${start}-${end} of ${lines.length})\n\n${chunk.join("\n")}${more}`;
  }

  async search(query: string, folder = "", maxResults = 15): Promise<string> {
    this.log("search", folder || undefined); // the query itself may be personal data: not logged
    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return "Empty query.";
    const snap = await this.backend.snapshot();
    const results: { score: number; rel: string; hits: string[] }[] = [];
    for (const rel of visibleFiles(this.member, [...snap.keys()], folder)) {
      const text = snap.get(rel)!;
      const hay = `${rel}\n${text}`.toLowerCase();
      if (!terms.every((t) => hay.includes(t))) continue;
      const hits = text
        .split("\n")
        .map((line, i) => [i + 1, line] as const)
        .filter(([, line]) => terms.some((t) => line.toLowerCase().includes(t)))
        .slice(0, 4)
        .map(([i, line]) => `  ${i}: ${line.trim().slice(0, 200)}`);
      const score = terms.reduce((s, t) => s + hay.split(t).length - 1, 0) + (terms.some((t) => rel.toLowerCase().includes(t)) ? 20 : 0);
      results.push({ score, rel, hits });
    }
    if (!results.length) return `No matches for '${query}'.`;
    results.sort((a, b) => b.score - a.score);
    const shown = results.slice(0, maxResults);
    return [`${results.length} matching files (showing ${shown.length}):`, ...shown.map((r) => `\n${r.rel}\n${r.hits.join("\n")}`)].join("\n");
  }

  private refusal(level: Member["write"]) {
    try {
      requireLevel(this.member, level);
    } catch (e) {
      const hint = this.member.write === "flag" ? " Use raise_flag to propose the change instead." : "";
      throw new AccessError(`${(e as Error).message}${hint}`);
    }
  }

  async appendToFile(path: string, content: string, reason: string): Promise<string> {
    this.refusal("append");
    const rel = normalizePath(path);
    const nope = `${rel}: not found or you can't write there.`;
    if (!canWrite(this.member, rel)) return nope;
    const block = `\n\n<!-- added by ${this.member.name} via context-mcp, ${today()}: ${mdCell(reason)} -->\n${content.trim()}\n`;
    try {
      await this.backend.writeFile(
        rel,
        (cur) => {
          if (cur === null) throw new WriteRefused(nope);
          return cur.replace(/\n+$/, "") + block;
        },
        this.commitMessage(`${rel}: ${reason}`),
        this.author,
      );
    } catch (e) {
      if (e instanceof WriteRefused) return e.message;
      throw e;
    }
    this.log("append_to_file", rel);
    return `Appended to ${rel} and committed as ${this.member.name}.`;
  }

  async createFile(path: string, content: string, reason: string): Promise<string> {
    this.refusal("create");
    const rel = normalizePath(path);
    if (!rel.endsWith(".md")) return "Only .md files can be created.";
    if (!canWrite(this.member, rel)) return `${rel}: you can't write there.`;
    try {
      await this.backend.writeFile(
        rel,
        (cur) => {
          if (cur !== null) throw new WriteRefused(`${rel} already exists: use append_to_file.`);
          return content.replace(/\n+$/, "") + "\n";
        },
        this.commitMessage(`${rel}: create, ${reason}`),
        this.author,
      );
    } catch (e) {
      if (e instanceof WriteRefused) return e.message;
      throw e;
    }
    this.log("create_file", rel);
    return `Created ${rel} and committed as ${this.member.name}.`;
  }

  // Members can raise flags without being able to read the flag queue (it holds sensitive notes).
  async raiseFlag(entity: string, change: string, kind = "update"): Promise<string> {
    this.refusal("flag");
    const rel = normalizePath(this.tenant.flagsFile);
    const section = "## Raised via Context MCP";
    const row = `| ${today()} | ${mdCell(entity)} | ${mdCell(kind)} | ${mdCell(change)} | ${mdCell(this.member.name)} | open |\n`;
    await this.backend.writeFile(
      rel,
      (cur) => {
        let text = cur ?? `# ${stem(rel)}\n\nChanges proposed for confirmation.\n`;
        if (!text.includes(section))
          text = `${text.replace(/\n+$/, "")}\n\n${section}\n\n| Date | Entity | Type | What changed / conflict | Said by | Status |\n|---|---|---|---|---|---|\n`;
        return text.replace(/\n+$/, "") + "\n" + row;
      },
      this.commitMessage(`flag: ${entity}: ${change.slice(0, 60)}`),
      this.author,
    );
    this.log("raise_flag", rel);
    return `Flag raised in ${rel} for a founder to confirm, committed as ${this.member.name}.`;
  }

  // ------------------------------------------------------------ skills as prompts

  /** The vault's skills: `<dir>/*.md` and `<dir>/<name>/SKILL.md`. First name wins. */
  private async promptPaths(): Promise<Map<string, string>> {
    const files = await this.allFiles();
    const found = new Map<string, string>();
    for (const dir of this.tenant.promptDirs) {
      const base = normalizePath(dir) + "/";
      for (const f of files.filter((p) => p.startsWith(base)).sort()) {
        const rest = f.slice(base.length).split("/");
        const name = rest.length === 1 && rest[0].endsWith(".md") ? rest[0].slice(0, -3) : rest.length === 2 && rest[1] === "SKILL.md" ? rest[0] : null;
        if (name && !found.has(name)) found.set(name, f);
      }
    }
    return found;
  }

  async prompts(): Promise<Prompt[]> {
    const found = await this.promptPaths();
    const texts = await Promise.all([...found.values()].map((p) => this.backend.readFile(p)));
    return [...found].map(([name, path], i) => ({
      name,
      path,
      description: (splitFrontmatter(texts[i]?.text ?? "").description ?? `The /${name} workflow from this vault.`).slice(0, 300),
    }));
  }

  async prompt(name: string, input = ""): Promise<string> {
    const path = (await this.promptPaths()).get(name);
    if (!path) throw new AccessError(`No prompt named ${name}.`);
    this.log("prompt", path);
    const { body } = splitFrontmatter((await this.backend.readFile(path))?.text ?? "");
    return body + PROMPT_NOTE + (input ? `\n\n---\nInput:\n${input}` : "");
  }
}
