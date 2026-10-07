---
type: use-case
project: "[[context-mcp]]"
last_updated: 2026-10-07
status: confirmed by Dan 2026-10-07 (answers to the six questions folded in); compliance details need legal review
---

# Context MCP: Use Case

← [[context-mcp]] · plan: [[v2-hosted-plan]] · handoff: [[handoff]] · compliance: [[compliance]]

✅ = Dan confirmed. ❓ = my assumption, still needs a yes/no.

## The one-liner
Context made easy to use wherever the client already is. Any agent (Claude, ChatGPT, Groq,
Hermes, whatever they use) plugs into the client's context folder after a sign-in, and every
session makes that context richer. ✅

## What it is and isn't
- ✅ **It does NOT replace the always-on assistant (Hermes).** It's an added benefit that sits
  beside it: the portable context layer. Hermes can use it too.
- ✅ **Agent-agnostic.** The client's own agent (ChatGPT, Claude, Groq, …) uses their context to
  give a better experience. We don't tie them to one model vendor.
- ✅ **Tools next to context.** Easy access to their tools via Composio, alongside the context.
  ❓ How: expose Composio's MCP next to ours (client adds two connectors), or proxy/bundle it
  behind our entry point. Decide after v2 core works; don't build before Dan chooses.
- ✅ **Snowball effect.** Using it builds the context: agents write back what they learn
  (additive, attributed, committed to the client's repo), so the vault gets better with every
  conversation. This is the main value claim, so write-back must be easy and safe.

## Principle: one entry point per vault ✅
Each vault gets its **own** endpoint (e.g. `https://<vault>.context.<domain>/mcp`) and its own
sign-in audience. A login for one vault can never reach another vault's context: not for clients,
and **not for Dan as operator by default**. Isolation is a product feature and a compliance
control, so it's tested, not assumed. Dan's own vault is just another vault with its own entry.

## Users (v2 scope)
| User | Scope now | Notes |
|---|---|---|
| Dan | His own vault, via its own entry point ✅ | Not default-visible inside client vaults |
| Rishab | Growify vault, **first test client** ✅ | Everything except Disha's private `self/` |
| Disha | Growify vault ✅ | Mirror: Rishab's `self/` hidden |
| Growify team / employees | **Not yet** ✅ | Founders and senior management only for now. The access model (flag-only role, deny lists) stays built in as the foundation for employees later |
| Future clients | Later, paid ✅ | Same shape, one vault each |

## Must-have for v2
1. ✅ Sign in on any new device, web, phone, desktop, and get the right context. Everyone uses
   Google accounts ✅, so Google is the sign-in.
2. ✅ Works from claude.ai web/mobile and **other agents** (ChatGPT etc.): standard remote MCP
   with OAuth, no client-specific hacks. ❓ Verify ChatGPT and Groq connector support in practice
   during Phase 4 (they have their own connector rules); don't promise per-vendor until tested.
3. ✅ One entry point per vault, strict isolation.
4. ✅ Per-person permissions (founders vs each other's `self/`; employee role built but unused).
5. ✅ Writes: additive, attributed, committed to the client's repo; founders can create, flagged
   items need a founder's confirmation.
6. ✅ No per-client server for Dan. Cost per tenant folded into the monthly fee ✅.
7. ✅ **GDPR-compliant and compliance-savvy from the start** (see [[compliance]]). It's a design
   constraint, not a later checklist.

## Nice-to-have
Stripe billing + self-serve signup, admin UI, usage/audit view for the client, Composio bundling,
digest/ontology refresh via a GitHub Action in the client repo, non-GitHub vault backends,
employee rollout.

## Out of scope for v2
Always-on assistant behaviour (Discord, voice capture, scheduled debriefs, Airtable/Workflowy pulls):
that stays Hermes. Employee access. Running vault scripts remotely. Replacing Obsidian/GitHub sync.

## Success tests
- Dan signs in on his phone and his own vault answers a question, no Hetzner box involved.
- Rishab does it on a fresh device in under 5 minutes without Dan's help.
- A Growify founder login cannot see the other founder's `self/`; a login for vault A returns
  nothing from vault B (automated isolation test).
- Same vault works from two different agents (e.g. claude.ai and one non-Claude agent).
- An agent writes something useful back and it appears as an attributed commit in the repo.
- Operator (Dan) cannot read a client vault without being an explicit member of it ❓ confirm.
- Cost per tenant measured after first deploy; confirm the monthly fee covers it.

## Risks
- **Compliance:** Dan is a processor of a client's personal data; needs a DPA, sub-processor list,
  EU-region handling, retention rules. See [[compliance]]. Legal review needed before charging.
- **Scope confusion:** pitch it as the context layer *next to* Hermes, not a replacement.
- **Agent support varies:** each vendor's connector rules differ (auth, transport, tool limits).
- **Write-back quality:** a snowballing vault can also accumulate junk; flag/confirm loop and
  attribution are the mitigation.
- **Search** on GitHub API is weak, and an index of content conflicts with the minimal-storage
  rule in [[compliance]]. Decide the trade-off in Phase 2.
- Composio route unresolved (above).

## Decisions made 2026-10-07 (round 2)
- ✅ Operator (Dan) has **zero default access** to client vaults; break-glass only if the client grants it, and it's logged.
- ✅ Composio is **not bundled**; it was an example. The point is plug-and-play: the client's agent
  uses their context and their own tools without re-explaining or re-entering credentials.
- ✅ Audit log retention: 12 months.
- ✅ Growify is Indian, Dan is UK-based: treat as **UK GDPR + EU GDPR + India DPDP Act**; default to EU/UK data handling.

## Open questions (remaining)
1. **Credentials in `.env` files (Dan: repos will hold `.env` files with tokens so the agent doesn't
   need to be told twice).** Conflicts with v1's always-hidden `.env` rule. Serving raw secrets to
   an agent puts them in the model vendor's context and logs, and they'd live in git history. Needs
   a deliberate design: see [[compliance]] "Secrets". Until decided, `.env` stays hidden.
2. Domain choice for per-vault hostnames (e.g. `<vault>.context.doanythingnow.co`).
3. Rishab's sign-off on what founders vs senior management can see.
4. Search approach under the no-storage rule: tarball-per-search (below), measure in Phase 2.
