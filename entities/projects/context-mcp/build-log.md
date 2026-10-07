---
type: build-log
project: "[[context-mcp]]"
last_updated: 2026-10-01
---

# Context MCP — Build Log

← [[context-mcp]]

## 2026-10-01 — v1 built and tested

**Ask (Dan):** "I love my context system but it only works for Claude Code. Could we make it an MCP —
something someone can plug into? e.g. my client giving access to an employee or his own Claude agent."

### Options considered

| Option | Verdict |
|---|---|
| Share the GitHub repo | Everyone sees everything (incl. founder-private `self/`), and only Claude Code users benefit. |
| Package as a Claude Code plugin | Ships the skills but still Claude-Code-only. |
| Paste into a Claude Project | Static copy, goes stale, no write-back. |
| **MCP server over the vault** ✅ | Works in any MCP client, enforces per-person access, writes back via git. |

### Design decisions

- **One generic server, one config per vault.** Same code for Dan's vault, Growify, every future client.
- **The vault stays the source of truth.** Server reads files directly; writes are git commits. GitHub sync + Obsidian keep working unchanged.
- **`get_map` first.** Returns the vault's own `CLAUDE.md` + orientation files, so the ICM routing (Map → Rooms → Tools) carries over to any agent with zero re-explaining.
- **Per-person tokens → globs + write level.** `read`/`deny` globs (deny wins), and `none` < `flag` < `append` < `create`. Hidden files answer "not found", so their existence isn't confirmed.
- **Additive-only writes.** No edit/overwrite tool exists. Append adds an attribution comment (`<!-- added by X via context-mcp, date: reason -->`). Employees are flag-only — matches Growify's `_flags.md` human-in-the-loop rule. Employees can *raise* flags but can't *read* the flag queue (it holds sensitive notes).
- **Always-hidden:** dot-paths (`.git`, `.claude`, `.obsidian`), `.env`, keys, `secrets*`, `credentials*`.
- **Skills become MCP prompts** (`/meeting`, `/wrap`, …), with a note telling the agent to skip script/git/sub-agent steps — the server commits for it.
- **Audit log** (JSONL): every call, who, what path. Good for client trust.
- **Tokens stored hashed** (SHA-256), shown once at creation, revocable.
- **Bearer-token auth now, OAuth later.** Tokens cover Claude Code, Claude Desktop, Cursor, Hermes. claude.ai web/mobile custom connectors need OAuth — deferred until a client actually wants that.

### Tech

Python 3.14 venv, `mcp` SDK 2.2 (`MCPServer`, formerly FastMCP), streamable HTTP (stateless, JSON
responses), uvicorn. ~400 lines. Systemd unit + Caddy (auto-HTTPS) for deployment.

### Tests (against a throwaway clone of the Growify vault — real repo untouched)

- Unauthenticated → 401. `/health` open.
- Employee: `founders/` invisible; `_team-restructure.md` (salaries / notice lists) → "not found"; `_flags.md` unreadable; append/create refused with a clear message; `raise_flag` works and commits as "Growify team".
- Rishab: full read except Disha's `self/`; append + create commit with author "Rishab Mehra".
- `../../etc/passwd` → "outside the vault". `.git/config` → not found.
- Prompts: 5 Growify skills listed; `/meeting` returns the skill + MCP note + input.
- **Real agent test:** `claude -p` (Haiku) connected as employee answered "who handles escalations + what's the process" correctly via search/read; asked about the restructure plan, it only reached the public org-structure file.

### Gotchas

- `mcp` 2.x renamed `FastMCP` → `MCPServer`; tool exceptions are hidden from the client unless they subclass `ToolError`.
- Vault repos are owned by other users → server runs git with `-c safe.directory=<vault>`; in production run the service *as* the vault owner.
- DNS-rebinding protection rejects unknown Host headers: set `allowed_hosts` once on a public domain.
- Remote agents can't run the vault scripts, so `_digest.md` / `_ontology.md` only refresh from the owner's sessions or GitHub Actions.
