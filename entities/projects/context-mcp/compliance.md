---
type: compliance
project: "[[context-mcp]]"
last_updated: 2026-10-07
status: engineering notes, NOT legal advice. Get a lawyer to review the DPA/terms before charging.
---

# Context MCP: Compliance (GDPR first)

← [[context-mcp]] · [[use-case]] · [[handoff]]

Dan's requirement: be GDPR-compliant and compliance-savvy with any other regimes. Context vaults
hold personal data (people files, meeting notes, HR-adjacent notes, Disha's/Rishab's `self/`),
so this shapes the architecture.

## Roles
- **Client (e.g. Growify)** = data controller. They decide what goes in the vault.
- **DoAnythingNow (Dan)** = processor: runs the service on the client's instruction.
- **Sub-processors:** Cloudflare (hosting), Google (sign-in identity), GitHub (vault storage, which
  the client already uses). Plus whichever AI vendor the client chooses to connect; that's the
  client's own choice and processing, not ours. ❓ Say this clearly in the terms.

## Engineering rules (build to these)
1. **Don't store vault content.** The vault stays in the client's GitHub repo; the Worker reads on
   demand. No copies in KV/D1/R2. Any cache must be short-lived, per-tenant and in-memory (or
   encrypted with a per-tenant key). This conflicts with a full-text search index, so decide
   deliberately.
2. **Data minimisation for what we do store:** tenant config, member emails, role/globs, audit log.
   Audit rows hold who/tool/path/time, **never file contents**.
3. **Isolation per vault:** one entry point and one data scope per vault; tokens bound to a single
   vault (audience/resource indicator); automated cross-tenant test in CI.
4. **Operator has no default access** to client vaults; break-glass only with client consent, logged.
5. **EU/UK residency:** pin data to the EU (Cloudflare jurisdiction/data-localisation options) and
   avoid sending content anywhere else. Verify the actual options before promising.
6. **Retention + erasure:** audit log kept 12 months (Dan, 2026-10-07);
   off-boarding a member or tenant deletes their rows; erasure of vault content is the client's
   repo, which we don't copy.
7. **Security:** TLS everywhere; secrets (GitHub App key, OAuth secret) in Cloudflare secrets only;
   least-privilege GitHub App (only the selected repo, contents read/write); short-lived tokens;
   no tokens or content in logs.
8. **Breach process:** documented, with the controller notified without undue delay (GDPR gives
   72h to the regulator; the DPA should set a faster notice to the client).
9. **No model training** and no secondary use of client data by us. Say it in the terms.

## Paperwork to produce (needs a lawyer's review)
- Data Processing Agreement (Art. 28) with each client; sub-processor list; international-transfer
  basis where relevant (SCCs/UK IDTA/adequacy).
- Privacy notice + terms for the service; security overview one-pager.
- Record of processing activities; DPIA if the client's data is sensitive (HR/health).
- Data-subject request process (access/erasure routes through the client as controller).

## Regimes
UK GDPR (Dan is UK-based) and EU GDPR; India DPDP Act (Growify is Indian, staff data in India). Cross-border transfer basis UK↔India↔EU to be set in the DPA. Later: SOC 2 / ISO 27001
later if enterprise clients ask. Don't claim certifications we don't hold.

## Secrets in vaults (DECIDED 2026-10-07: option 1, broker don't reveal)
Dan wants repos to hold `.env` files with tokens/credentials so an agent can use the client's tools
(e.g. Composio) without being told twice. Risks to design around, not ignore:
- A secret the MCP serves as text lands in the AI vendor's context window and logs, outside our control.
- Secrets in git history are hard to revoke and widen who can see them (anyone with repo access).
- Breaks the "least data in the repo" posture of the processor role.
Options, safest first: (1) **broker, don't reveal:** the MCP calls the tool with the credential
server-side and returns only results, so the agent never sees the secret; (2) per-vault encrypted
secret store (per-tenant key, EU), exposed only to owner roles, never in tool output; (3) serve
`.env` text to the owner's agent (simplest, weakest; client must accept the risk in writing).
**Dan chose option 1:** the MCP uses credentials server-side and the agent never sees them. Credentials live in a per-vault encrypted store (option 2) rather than served as `.env` text. Raw `.env`/credentials files stay always-hidden. Implementation details (how a client registers a tool + its credential, which tool calls are brokered) are still to design.

## Open
- EU region choice; escalation/notice period to clients on a breach; broker design (Phase 5+).
