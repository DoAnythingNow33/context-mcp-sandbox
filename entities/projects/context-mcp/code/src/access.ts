// Access control for a context vault. Ported from v1 (context_mcp/server.py) with identical
// semantics: deny wins, "*" also matches "/", dot-paths and secrets are never visible.

export const WRITE_LEVELS = ["none", "flag", "append", "create"] as const;
export type WriteLevel = (typeof WRITE_LEVELS)[number];

export interface Member {
  email: string;
  name: string;
  read: string[];
  deny: string[];
  write: WriteLevel;
  writePaths: string[];
}

// Never served, whatever a member's globs say.
export const ALWAYS_DENY = ["**/.env", "**/*.key", "**/*.pem", "**/credentials*", "**/secrets*"];

export class AccessError extends Error {}

const cache = new Map<string, RegExp>();

// fnmatch-style: "*" and "**" both match any run of characters including "/", "?" one char.
function globToRegex(glob: string): RegExp {
  let re = cache.get(glob);
  if (re) return re;
  let out = "";
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === "*") {
      while (glob[i + 1] === "*") i++;
      out += ".*";
    } else if (c === "?") out += ".";
    else out += c.replace(/[.+^${}()|[\]\\]/g, "\\$&");
  }
  re = new RegExp(`^${out}$`, "s");
  cache.set(glob, re);
  return re;
}

export const matches = (rel: string, globs: string[]) => globs.some((g) => globToRegex(g).test(rel));

/** Normalise a user-supplied path; throws if it escapes the vault. */
export function normalizePath(input: string): string {
  const parts: string[] = [];
  for (const seg of input.trim().replaceAll("\\", "/").split("/")) {
    if (seg === "" || seg === ".") continue;
    if (seg === "..") {
      if (!parts.length) throw new AccessError(`${input}: outside the vault`);
      parts.pop();
    } else parts.push(seg);
  }
  return parts.join("/");
}

export function canRead(m: Member, rel: string): boolean {
  if (rel.split("/").some((p) => p.startsWith("."))) return false;
  if (matches(rel, ALWAYS_DENY) || matches(rel, m.deny)) return false;
  return matches(rel, m.read);
}

export const canWrite = (m: Member, rel: string) => canRead(m, rel) && matches(rel, m.writePaths);

export const writeLevel = (m: Member) => WRITE_LEVELS.indexOf(m.write);

export function requireLevel(m: Member, level: WriteLevel): void {
  if (writeLevel(m) < WRITE_LEVELS.indexOf(level))
    throw new AccessError(`Your access is "${m.write}"; this needs "${level}".`);
}

export const visibleFiles = (m: Member, allPaths: string[], under = ""): string[] => {
  const base = under ? normalizePath(under) : "";
  return allPaths
    .filter((p) => (!base || p === base || p.startsWith(base + "/")) && canRead(m, p))
    .sort();
};
