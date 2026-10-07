---
entity: Context MCP
type: snapshot
last_updated: 2026-10-07
current_state: "Turns a Context 2.0 / ICM vault into an MCP server so anyone's AI can plug into it — not just Claude Code rooted in the folder. v1 built and tested 2026-10-01 at /home/hermes/context-mcp on the Hetzner box (Python, mcp SDK 2.2, streamable HTTP). Per-person bearer tokens map to read/deny globs + a write level (none/flag/append/create); writes are additive and each one is a git commit under that person's name; every call is audit-logged. Vault skills (/meeting, /wrap, /pull-ip…) are served as MCP prompts. Tested against a throwaway clone of the Growify vault: employee token cannot see founders/ or the salary/notice-list file, path traversal blocked, flags/appends/creates commit correctly, and a real Claude agent answered a Growify question through it as an employee. Not yet deployed — runs locally only."
current_focus:
  - "v2 (decided 2026-10-07): hosted multi-tenant on Cloudflare Workers, OAuth sign-in so it works in claude.ai web/mobile, client's GitHub repo as the vault. First users: Dan + Rishab. Paid product, but no billing yet. See v2-hosted-plan, use-case, handoff. Phases 1–3 done 2026-10-07 (access core, GitHub backend, MCP tools on a Worker; 25 tests); live GitHub test pending a sandbox repo + PAT. Use case confirmed 2026-10-07: complements Hermes (not a replacement), agent-agnostic, snowballs context via write-back, one entry point per vault, GDPR by design, founders/senior management only at launch."
  - "Demo to Rishab once v2 is deployed: sign in on his phone, plus an employee login to show the permission split."
open_questions:
  - "Composio: sibling connector or bundled behind our entry point? Region + audit retention? Operator break-glass access? (use-case.md, compliance.md)"
  - "Which domain/subdomain hosts it (e.g. context.doanythingnow.co)?"
  - "Which Growify folders are safe for employees? v1 default = all of Growify/ except _team-restructure, _flags, _archive, _status. Meetings and people files may still hold sensitive notes — Rishab should sign off."
tensions:
  - "Wider access vs. vault trust: the more people write into the source of truth, the more it needs the flag-and-confirm loop to stay clean. Employees get flag-only for that reason."
  - "Remote agents can't run the vault's scripts (generate_digest, build_ontology) — the map and digest can drift unless the owner's own sessions or GitHub Actions keep regenerating them."
next_actions:
  - "Dan: create Cloudflare account/token, domain, Google OAuth client, GitHub App (handoff.md)"
  - "Agent: live test against a sandbox repo once Dan provides it, then Phase 4 OAuth + Google sign-in"
  - "Get Rishab's sign-off on the employee deny list"
---

# Context MCP

**Relationship:** DoAnythingNow product/infrastructure — makes every client's context vault portable.
**Role:** Builder/operator
**Code:** `/home/hermes/context-mcp` (on the Hetzner box) — see its `README.md`

## Why

The context system only worked inside Claude Code opened in the vault folder. Clients want to give
their team, or their own Claude, access to that context — with founder-private parts kept private.
MCP is the standard plug: any MCP-capable AI connects with one URL + token.

## Files in this folder

- [[use-case]]: confirmed use case, need vs want, success tests (v2)
- [[compliance]]: GDPR/engineering rules and paperwork for the hosted service
- [[v2-hosted-plan]]: hosted architecture, decisions, phases (v2)
- [[handoff]]: **start here when picking the build up**, status/blockers/gotchas
- [[build-log]] — how it was built, decisions and why, test results
- [[client-rollout-sop]] — step-by-step to turn it on for a client

## People

- [[growify]] — first client (Rishab, Disha, team)

## Meetings
