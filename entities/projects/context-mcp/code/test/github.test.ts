import { describe, expect, it } from "vitest";
import { GitHubError, GitHubVault, WriteRefused } from "../src/github";
import { FakeGitHub } from "./fake-github";

const longPath = `Growify/meetings/${"a-very-long-meeting-title-".repeat(5)}2026-10-01.md`;
const seed = {
  "CLAUDE.md": "# Map\n",
  "Growify/people/rishab.md": "# Rishab ✓ — founder\n",
  "Growify/_flags.md": "# Flags\n",
  "Growify/logo.png": "binary",
  [longPath]: "long one",
};

function setup(token = "test-token") {
  const gh = new FakeGitHub(seed);
  const vault = new GitHubVault({ owner: "acme", repo: "vault", branch: "main", token: async () => token, fetch: gh.fetch });
  return { gh, vault };
}

const rishab = { name: "Rishab Mehra", email: "rishab@growify.example" };

describe("GitHubVault", () => {
  it("lists text files only, no directories", async () => {
    const { vault } = setup();
    expect(await vault.listFiles()).toEqual(["CLAUDE.md", "Growify/_flags.md", longPath, "Growify/people/rishab.md"].sort());
  });

  it("reads UTF-8 text with its sha; missing files are null", async () => {
    const { vault } = setup();
    expect((await vault.readFile("Growify/people/rishab.md"))?.text).toBe("# Rishab ✓ — founder\n");
    expect(await vault.readFile("nope.md")).toBeNull();
  });

  it("snapshot holds every text file from one tarball request, incl. pax long names", async () => {
    const { gh, vault } = setup();
    const snap = await vault.snapshot();
    expect([...snap.keys()].sort()).toEqual(["CLAUDE.md", "Growify/_flags.md", longPath, "Growify/people/rishab.md"].sort());
    expect(snap.get(longPath)).toBe("long one");
    expect(snap.get("Growify/people/rishab.md")).toBe("# Rishab ✓ — founder\n");
    expect(gh.requests).toEqual(["GET /repos/acme/vault/tarball/main"]);
  });

  it("creates and appends as commits authored by the member", async () => {
    const { gh, vault } = setup();
    await vault.writeFile("Growify/new.md", (cur) => (cur === null ? "hello\n" : cur), "create", rishab);
    await vault.writeFile("Growify/new.md", (cur) => cur + "more\n", "append", rishab);
    expect(gh.files.get("Growify/new.md")).toBe("hello\nmore\n");
    expect(gh.commits.map((c) => [c.path, c.message, c.author.name])).toEqual([
      ["Growify/new.md", "create", "Rishab Mehra"],
      ["Growify/new.md", "append", "Rishab Mehra"],
    ]);
  });

  it("re-applies an append when someone else commits in between (409)", async () => {
    const { gh, vault } = setup();
    let raced = false;
    gh.beforePut = (p) => {
      if (!raced) {
        raced = true;
        gh.set(p, gh.files.get(p) + "theirs\n");
      }
    };
    await vault.writeFile("Growify/_flags.md", (cur) => cur + "ours\n", "flag", rishab);
    expect(gh.files.get("Growify/_flags.md")).toBe("# Flags\ntheirs\nours\n");
    expect(gh.commits).toHaveLength(1);
  });

  it("a create that loses a race sees the new file on retry (422)", async () => {
    const { gh, vault } = setup();
    let raced = false;
    gh.beforePut = (p) => {
      if (!raced) {
        raced = true;
        gh.set(p, "someone else's\n");
      }
    };
    const create = (cur: string | null) => {
      if (cur !== null) throw new WriteRefused("already exists");
      return "mine\n";
    };
    await expect(vault.writeFile("Growify/x.md", create, "create", rishab)).rejects.toThrow(WriteRefused);
    expect(gh.files.get("Growify/x.md")).toBe("someone else's\n");
  });

  it("surfaces auth failures as GitHubError with status", async () => {
    const { vault } = setup("wrong");
    const err = await vault.listFiles().catch((e) => e);
    expect(err).toBeInstanceOf(GitHubError);
    expect(err.status).toBe(401);
  });
});
