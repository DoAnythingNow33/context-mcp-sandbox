---
type: plan
project: "[[context-mcp]]"
last_updated: 2026-10-07
updated_after: "Dan confirmed use case + compliance constraints"
---

# Context MCP v2: hosted, sign-in, any device

← [[context-mcp]] · v1 notes: [[build-log]], [[client-rollout-sop]]

**Goal (Dan, 2026-10-07):** paid product. Clients sign in on any new device (web, mobile,
desktop, Claude Code) and get the context they're allowed to see. No per-client servers,
no Hetzner upkeep. First users: Dan and Rishab (Growify), but built multi-tenant from day one.

## Decisions

| Area | Choice | Why |
|---|---|---|
| Vault home | Client's GitHub repo (read/write via a GitHub App) | Client owns data; no git/filesystem on our side; Obsidian + GitHub sync keep working |
| Runtime | Cloudflare Workers (TypeScript) | No server to patch, ~free at this scale, global, supports remote MCP + OAuth |
| MCP auth | OAuth 2.1 via `@cloudflare/workers-oauth-provider` | Required for claude.ai web/mobile custom connectors; also works in Desktop/Claude Code/Cursor |
| Login (IdP) | Google (email identity) | Confirmed: all users have Google accounts; email maps to a member/role |
| Tenants/roles | **One entry point per vault** (own hostname + own OAuth audience); config in a per-vault store (Durable Object SQLite in an EU jurisdiction, or D1 per vault): repo, member email, read/deny globs, write level | Isolation is a product + GDPR requirement; v1 model (`configs/*.yaml`) carries over |
| Writes | Additive only, committed via GitHub API as the user, one commit per write, straight to the default branch; no clone, no end-of-session push (differs from the local-clone + push workflow of v1 and Dan's own sessions) | Same levels as v1; conflicts rare because additive; 409 retry |
| Audit | Per-vault table (who, tool, path, time; **never content**), fixed retention | Client trust + GDPR minimisation |
| Freshness | GitHub Action in client repo regenerates `_digest.md` / ontology on push | Remote agents can't run scripts |
| Billing | Later: Stripe per-tenant plan; schema has `tenant.plan` from start | Don't block Dan/Rishab on it |

## What carries over from v1 (`/home/hermes/context-mcp`)
Read/deny globs (deny wins), write levels none<flag<append<create, always-hidden files,
"not found" for hidden paths, path-traversal guard, additive-only writes with attribution comment,
skills served as MCP prompts, audit log, `get_map` first.

## Phases
1. **Core (no accounts needed):** access-control module + tests, ported from v1. ✅
2. **GitHub backend:** list/read/search/commit via App installation token; test on a throwaway repo. ← built, fake-GitHub tested; live test pending
3. **MCP tools + prompts** on a Worker, `wrangler dev` locally with a fake IdP. ✅ 2026-10-07
4. **OAuth + Google login**, then real deploy for Dan's vault; connect from claude.ai web + phone.
5. **Growify:** install the GitHub App on Rishab's repo, get employee-deny sign-off, invite users.
6. Admin (tenant/user management), Stripe, GitHub Action template.

## Needed from Dan (accounts only he can create)
- Cloudflare account (likely Workers Paid, $5/mo: search measured over the free 10 ms CPU cap) and `wrangler login` / API token
- A domain or subdomain (e.g. context.doanythingnow.co) on Cloudflare DNS
- Google Cloud OAuth client (consent screen + client id/secret)
- GitHub App (I'll give exact settings) installed on Dan's vault, later Growify's
- Rishab's sign-off on the employee deny list (carried from v1)

## Constraints added 2026-10-07 (see [[use-case]], [[compliance]])
- **Agent-agnostic:** plain remote MCP + OAuth so Claude, ChatGPT, Groq etc. can connect; verify each in Phase 4.
- **No vault content stored by us** (no KV/D1/R2 copies; short-lived in-memory cache only). So no
  push-webhook search index unless Dan accepts the trade-off; start with GitHub API tree + fetch.
- **Operator has no default access** to client vaults.
- **EU/UK data pinning** for anything we do store.
- Founders + senior management only at launch; employee role stays built, switched off.
- Composio: undecided whether bundled or a sibling connector; not in v2 core.

## Open
- Search under the no-storage rule: fetch the repo tarball (1 GitHub request), gunzip + grep in memory, discard. Growify = 284 text files / 0.8 MB, Dan's vault = 353 md / 1.6 MB. Measured 2026-10-07 (CPU only, network not yet): 40–60 ms Dan, ~12 ms Growify. Fine for latency; fallback = opt-in encrypted per-vault index.
- Credentials from repo `.env`: see compliance.md "Secrets".
- Composio route. Region choice. Audit retention.
