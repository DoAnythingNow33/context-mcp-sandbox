---
type: handoff
project: "[[context-mcp]]"
last_updated: 2026-10-07
---

# Context MCP: Agent Handoff

← [[context-mcp]] · use case: [[use-case]] · plan: [[v2-hosted-plan]] · v1: [[build-log]]

**Read this first if you're picking the build up.** Update the "Status" and "Log" sections when you
stop. Keep it short and factual.

## Status (2026-10-07)
- **v1 (Python, local, working, tested, never deployed):** `/home/hermes/context-mcp` on the Hetzner box.
  Per-person bearer tokens, read/deny globs, write levels, git commits as the user. Reference
  implementation for behaviour. `README.md` there.
- **v2 (TypeScript, Cloudflare Workers, hosted, sign-in):** `entities/projects/context-mcp/code/` in this repo (symlinked at `/home/hermes/context-mcp-cloud`). `.dev.vars` and `node_modules/` are gitignored and exist only on the box.
  - ✅ Phase 1: `src/access.ts` (ported access control) + `test/access.test.ts` (7 passing).
  - 🟡 Phase 2: `src/github.ts` (`GitHubVault`: listFiles via tree API, readFile via Contents API,
    `snapshot()` = tarball → gunzip + untar in memory for search, `writeFile(path, transform)` = Contents
    PUT authored as the member, re-reads + re-applies on 409/422). Tested against `test/fake-github.ts`
    (sha-checked writes, real pax tar.gz): 7 tests. **Not yet run against real GitHub:** needs a
    fine-grained PAT on a throwaway repo (Contents read/write, that repo only).
    Search measured: gunzip+untar+grep = 40–60 ms (Dan's vault, 363 files, 828 KB gz), ~12 ms (Growify, 279 files).
    That's over the Workers **free** plan's 10 ms CPU limit, so expect Workers Paid ($5/mo); confirm on deploy.
  - ✅ Phase 3: `src/vault.ts` (v1 tools ported: get_map, list_files, read_file, search, append_to_file,
    create_file, raise_flag; vault skills as prompts, listed on demand), `src/server.ts` (stateless MCP
    server built per request for one member of one vault, JSON responses), `src/worker.ts` (vault chosen
    by hostname, member by sign-in; `createApp(deps)` is the seam Phase 4 swaps OAuth into).
    `test/worker.test.ts`: real MCP client → app, 11 tests incl. cross-tenant isolation (mutation-checked:
    a membership bypass fails it), operator zero access, audit holds no content/queries. **25/25 total.**
    Ran under `wrangler dev` (workerd): handshake, tools/list, 401 without login, calls reach real GitHub.
    Bundle 247 KB gz. Sign-in is a dev stub (`Bearer dev:<email>`, only when `DEV_AUTH=1`).
    Audit currently goes to `console.log`; Phase 4 needs the per-vault EU table.
  - ⏳ Phase 4: OAuth + Google sign-in, real deploy. Blocked on Dan's accounts (below).
- Use case **confirmed by Dan 2026-10-07** ([[use-case]]); compliance rules in [[compliance]]. Remaining open items are listed at the bottom of use-case.md.

## Blocked on Dan
Cloudflare account + API token/`wrangler login`; a domain/subdomain on Cloudflare DNS; a Google Cloud
OAuth client; a GitHub App on his vault (later Growify's); Rishab's sign-off on the employee deny list.
For the live Phase 2 test: an empty private throwaway repo (e.g. `context-mcp-sandbox`) + a fine-grained
PAT limited to it (Contents read/write). No GitHub connector exists in Claude's tools, so Dan creates both.

## How to run
```bash
cd /home/hermes/context-2.0-github/entities/projects/context-mcp/code
npm test            # vitest
npm run typecheck   # tsc --noEmit
cp .dev.vars.example .dev.vars   # set GITHUB_TOKEN + repo owner, then:
npx wrangler dev --port 8787     # POST /mcp with `Authorization: Bearer dev:<member email>`
```
**Gotcha:** `node`/`npm` are symlinks into `/root/.hermes/node`, so the `hermes` user can't run
them. Run npm as root, then `chown -R hermes:hermes /home/hermes/context-2.0-github/entities/projects/context-mcp/code`. Don't "fix"
by changing `/root` permissions without asking Dan.

## Design rules (don't change without Dan)
- Vault = the client's GitHub repo; it stays the source of truth. No local filesystem, no git binary.
- Access semantics must equal v1: **deny wins**; `*` also matches `/`; dot-paths + secrets always hidden;
  hidden files answer "not found" (never "forbidden", so existence isn't confirmed); `..` rejected.
- Writes are additive only (append/create/flag). No edit or delete tool. Employees: flag only.
- Always attribute: commit under the member's name; audit every call.
- Multi-tenant from day one (`tenant` + `plan` in the schema), no billing code yet.
- **One entry point per vault.** Own hostname + audience-bound tokens; a login for vault A must never return vault B data. Write an automated cross-tenant test before any deploy. The operator (Dan) has no default access to client vaults.
- **Don't store vault content** in KV/D1/R2/logs. Audit rows: who/tool/path/time only. Pin stored data to EU/UK. See [[compliance]].
- **Agent-agnostic:** standard remote MCP + OAuth; don't add Claude-only features. Test a non-Claude agent in Phase 4.
- **Secrets: decided, broker don't reveal.** The MCP calls tools with stored credentials server-side; agents never see them. Keep `.env`/credentials always-hidden. See [[compliance]] "Secrets".
- **Git model:** no clone, no local git. Every write is an immediate commit via the GitHub API (Contents API with sha; retry on 409), authored as the member. Dan's local clone/Obsidian/Hermes must pull. Auto-pull was fixed 2026-10-07 (see Log), so the box's clone now rebases onto GitHub. **Decided by Dan: agent writes commit directly to the default branch** (no review branch).
- v2 users are founders/senior management only; employee role (flag-only) stays built but unused.
- Never test against a real client repo. Use a throwaway clone (as v1 did).

## Decisions and why
Stored in [[v2-hosted-plan]] (table). The key one: Cloudflare Workers over a VPS, because the whole
point is no server upkeep (see the Oct 5 OOM incident in `docs/claude-code-discord-assistant.md`).

## Do not touch
- Growify's real repo and the `rishab` instance (Dan's rule from the Discord migration).
- The Hermes gateways. MCP complements them, it does not replace them (Dan, 2026-10-07).

## Log
- 2026-10-07 (r6): Phase 3 built: MCP tools/prompts on a Worker, 25/25 tests, runs under wrangler dev. Next: live GitHub test (needs sandbox repo + PAT), then Phase 4 OAuth. (Claude)
- 2026-10-07 (r5): Phase 2 backend built + tested on a fake GitHub (14/14 tests, typecheck clean). Search latency measured; Workers free tier likely too small. Next: live PAT test on a throwaway repo, then Phase 3. (Claude)
- 2026-10-07 (r4): direct commits confirmed. Fixed Vault Auto-Pull: it had skipped since 10-01 because the tree was dirty AND the branch diverged from the weekly self-heal Action commits (ff-only could never succeed). Committed + pushed the box work, rewrote `~/.hermes/scripts/vault-autopull.sh` to rebase --autostash, alert only on conflict, and nudge when work exists only on the box (backup: `.bak-20261007`). (Claude)
- 2026-10-07 (r3): secrets = broker; git model = API commits, no clone. (Claude)
- 2026-10-07 (r2): operator zero-access, Composio not bundled, audit 12mo, regimes UK/EU/India set. Open: .env secrets design, search approach. (Claude)
- 2026-10-07: Dan answered the use-case questions; use-case rewritten, compliance.md added, plan + handoff updated. (Claude)
- 2026-10-07: v2 plan written, Phase 1 built and tested; use case drafted for Dan to confirm. (Claude)
