// End to end: a real MCP client talking to the Worker app, with GitHub faked per vault.
// Mirrors the v1 tests (employee vs founder, hidden files, attribution) plus cross-tenant isolation.

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { beforeEach, describe, expect, it } from "vitest";
import type { Member } from "../src/access";
import { GitHubVault } from "../src/github";
import type { AuditEvent, Tenant } from "../src/vault";
import { createApp } from "../src/worker";
import { FakeGitHub } from "./fake-github";

const rishab: Member = { email: "rishab@growify.example", name: "Rishab Mehra", read: ["**"], deny: ["founders/Disha/self/**"], write: "create", writePaths: ["**"] };
const employee: Member = {
  email: "team@growify.example", name: "Growify team", write: "flag", read: ["Growify/**"], writePaths: ["Growify/**"],
  deny: ["Growify/people/_team-restructure.md", "Growify/_flags*", "Growify/_archive/**", "Growify/_status/**"],
};
const dan: Member = { email: "dan@doanythingnow.example", name: "Dan", read: ["**"], deny: [], write: "create", writePaths: ["**"] };

const tenant = (id: string, hostname: string, members: Member[]): Tenant => ({
  id, plan: "pilot", name: id, hostname, repo: { owner: "acme", repo: "vault", branch: "main" },
  mapFile: "CLAUDE.md", orientationFiles: ["Growify/_digest.md"], flagsFile: "Growify/_flags.md",
  promptDirs: [".claude/commands", ".claude/skills"], members,
});
const growify = tenant("growify", "growify.context.test", [rishab, employee]);
const danVault = tenant("dan", "dan.context.test", [dan]);

let gh: Record<string, FakeGitHub>;
let audit: AuditEvent[];

beforeEach(() => {
  audit = [];
  gh = {
    growify: new FakeGitHub({
      "CLAUDE.md": "# Growify map\nRead Growify/_digest.md first.\n",
      "Growify/_digest.md": "# Digest\nEscalations: Nitish.\n",
      "Growify/processes/escalations.md": "# Escalations\nNitish owns client escalations.\n",
      "Growify/people/_team-restructure.md": "# Restructure\nSalaries and escalation notice list.\n",
      "Growify/_flags.md": "# Flags\n\n| Date | x |\n|---|---|\n| 2026-09-01 | secret flag |\n",
      "founders/Rishab/self/goals.md": "# Rishab goals\n",
      "founders/Disha/self/goals.md": "# Disha private goals\n",
      ".claude/commands/meeting.md": '---\ndescription: "Log a meeting"\n---\nSummarise the meeting.\n',
      ".claude/skills/wrap/SKILL.md": "---\nname: wrap\n---\nWrap up the session.\n",
      ".env": "TOKEN=nope\n",
    }),
    dan: new FakeGitHub({ "CLAUDE.md": "# Dan's map\n", "self/goals.md": "# Dan private\n" }),
  };
});

const app = () =>
  createApp({
    tenantForHost: (h) => [growify, danVault].find((t) => t.hostname === h),
    authenticate: async (req) => req.headers.get("x-test-user") ?? undefined,
    backendFor: (t) => new GitHubVault({ ...t.repo, token: async () => "test-token", fetch: gh[t.id].fetch }),
    audit: (e) => audit.push(e),
  });

async function connect(host: string, email: string) {
  const handler = app();
  const client = new Client({ name: "test", version: "1" });
  const transport = new StreamableHTTPClientTransport(new URL(`https://${host}/mcp`), {
    fetch: (url, init) => handler(new Request(url, { ...init, headers: { ...Object.fromEntries(new Headers(init?.headers)), "x-test-user": email } })),
  });
  await client.connect(transport);
  const call = async (name: string, args: Record<string, unknown> = {}) => {
    const r = (await client.callTool({ name, arguments: args })) as { content: { text: string }[]; isError?: boolean };
    return { text: r.content[0].text, isError: !!r.isError };
  };
  return { client, call };
}

const post = (host: string, user?: string) =>
  app()(new Request(`https://${host}/mcp`, {
    method: "POST",
    headers: { "content-type": "application/json", accept: "application/json, text/event-stream", ...(user ? { "x-test-user": user } : {}) },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/list" }),
  }));

describe("entry point and isolation", () => {
  it("unknown host 404, no login 401, health open", async () => {
    expect((await post("evil.test", rishab.email)).status).toBe(404);
    expect((await post(growify.hostname)).status).toBe(401);
    expect((await app()(new Request("https://x/health"))).status).toBe(200);
  });

  it("a login for vault A gets nothing from vault B, and the operator has no default access", async () => {
    expect((await post(danVault.hostname, rishab.email)).status).toBe(401);
    expect((await post(growify.hostname, dan.email)).status).toBe(401);
    expect(gh.dan.requests).toEqual([]);
    expect(gh.growify.requests).toEqual([]);
  });

  it("each vault only ever reads its own repo", async () => {
    const { call } = await connect(danVault.hostname, dan.email);
    expect((await call("get_map")).text).toContain("Dan's map");
    expect(gh.growify.requests).toEqual([]);
  });
});

describe("employee (flag only)", () => {
  it("sees the business room only; hidden files read as not found", async () => {
    const { call } = await connect(growify.hostname, employee.email);
    const map = (await call("get_map")).text;
    expect(map).toContain("Growify team");
    expect(map).toContain("**flag**");
    expect(map).not.toContain("Growify map"); // CLAUDE.md is outside Growify/**
    const files = (await call("list_files")).text;
    expect(files).toContain("Growify/processes/escalations.md");
    expect(files).not.toMatch(/founders|_flags|_team-restructure|\.claude|\.env/);
    expect((await call("read_file", { path: "Growify/people/_team-restructure.md" })).text).toBe(
      "Growify/people/_team-restructure.md: not found or not accessible.",
    );
    expect((await call("read_file", { path: ".env" })).text).toContain("not found");
  });

  it("search skips hidden files", async () => {
    const { call } = await connect(growify.hostname, employee.email);
    const r = (await call("search", { query: "escalation" })).text;
    expect(r).toContain("Growify/processes/escalations.md");
    expect(r).not.toContain("_team-restructure");
  });

  it("can raise a flag but not append or create", async () => {
    const { call } = await connect(growify.hostname, employee.email);
    const a = await call("append_to_file", { path: "Growify/processes/escalations.md", content: "x", reason: "y" });
    expect(a.isError).toBe(true);
    expect(a.text).toContain("raise_flag");
    expect((await call("create_file", { path: "Growify/n.md", content: "x", reason: "y" })).isError).toBe(true);
    await call("raise_flag", { entity: "Nitish", change: "now also owns | billing", kind: "update" });
    const flags = gh.growify.files.get("Growify/_flags.md")!;
    expect(flags).toContain("secret flag"); // existing rows kept
    expect(flags).toContain("## Raised via Context MCP");
    expect(flags).toMatch(/\| Nitish \| update \| now also owns \\\| billing \| Growify team \| open \|/);
    expect(gh.growify.commits.at(-1)!.author.name).toBe("Growify team");
  });
});

describe("founder (create)", () => {
  it("reads everything except the other founder's self/", async () => {
    const { call } = await connect(growify.hostname, rishab.email);
    expect((await call("read_file", { path: "founders/Rishab/self/goals.md" })).text).toContain("Rishab goals");
    expect((await call("read_file", { path: "founders/Disha/self/goals.md" })).text).toContain("not found");
    expect((await call("read_file", { path: "Growify/people/_team-restructure.md" })).text).toContain("Salaries");
  });

  it("appends and creates as attributed commits; never overwrites", async () => {
    const { call } = await connect(growify.hostname, rishab.email);
    expect((await call("append_to_file", { path: "Growify/processes/escalations.md", content: "Disha backs up.", reason: "call 7 Oct" })).text).toContain(
      "committed as Rishab Mehra",
    );
    const esc = gh.growify.files.get("Growify/processes/escalations.md")!;
    expect(esc).toMatch(/^# Escalations\nNitish owns client escalations.\n\n<!-- added by Rishab Mehra via context-mcp, \d{4}-\d\d-\d\d: call 7 Oct -->\nDisha backs up.\n$/);
    await call("create_file", { path: "Growify/clients/new.md", content: "# New client", reason: "intro call" });
    expect(gh.growify.files.get("Growify/clients/new.md")).toBe("# New client\n");
    expect((await call("create_file", { path: "Growify/clients/new.md", content: "dupe", reason: "x" })).text).toContain("already exists");
    expect((await call("create_file", { path: "Growify/x.txt", content: "x", reason: "x" })).text).toBe("Only .md files can be created.");
    expect(gh.growify.commits.map((c) => c.author.email)).toEqual([rishab.email, rishab.email]);
    expect(gh.growify.commits[0].message).toBe(`Growify/processes/escalations.md: call 7 Oct\n\nvia context-mcp (${rishab.email})`);
  });

  it("rejects path traversal and paging works", async () => {
    const { call } = await connect(growify.hostname, rishab.email);
    const r = await call("read_file", { path: "../../etc/passwd" });
    expect(r.isError).toBe(true);
    expect(r.text).toContain("outside the vault");
    expect((await call("read_file", { path: "Growify/processes/escalations.md", max_lines: 1 })).text).toContain("call read_file with start_line=2");
  });

  it("serves vault skills as prompts", async () => {
    const { client } = await connect(growify.hostname, rishab.email);
    const { prompts } = await client.listPrompts();
    expect(prompts.map((p) => [p.name, p.description])).toEqual([
      ["meeting", "Log a meeting"],
      ["wrap", "The /wrap workflow from this vault."],
    ]);
    const p = await client.getPrompt({ name: "meeting", arguments: { input: "notes here" } });
    const t = (p.messages[0].content as { text: string }).text;
    expect(t.startsWith("Summarise the meeting.")).toBe(true);
    expect(t).toContain("through the context MCP server");
    expect(t.endsWith("Input:\nnotes here")).toBe(true);
  });
});

it("audit rows hold who/tool/path/time only, never content or queries", async () => {
  const { call } = await connect(growify.hostname, rishab.email);
  await call("search", { query: "salaries" });
  await call("append_to_file", { path: "Growify/processes/escalations.md", content: "SECRET CONTENT", reason: "private reason" });
  for (const e of audit) expect(Object.keys(e).every((k) => ["ts", "tenant", "member", "tool", "path"].includes(k))).toBe(true);
  expect(JSON.stringify(audit)).not.toMatch(/SECRET|salaries|private reason/);
  expect(audit.map((e) => e.tool)).toEqual(["search", "append_to_file"]);
});
