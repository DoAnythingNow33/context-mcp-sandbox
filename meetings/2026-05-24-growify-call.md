---
title: Growify — Call
type: meeting
date: 2026-05-24
attendees:
  - Daniel (DoAnythingNow)
  - Rishabh Mehra (Growify)
  - Disha Bhatnagar (Growify)
status: complete
---

← [[entities/people/growify]] | [[calendar/2026/Q2/may-2026]]

# Growify — Call — 24 May 2026

## Summary

Alignment call to confirm Phase 1 scope and lock the session schedule. Deliverables confirmed: Whimsical map, company-level + individual Obsidian/GitHub folders, group Claude Code setup session, prioritisation output. Key shift: Rishabh wants company-level folder architecture with access tiers, not just 4 individual folders — hosting pivoted from Obsidian-local to GitHub to solve the no-company-laptop problem for Chandika and Rohit. Session schedule locked around co-founder travel: Disha 31 May + 6 Jun, Chandika/Rohit 4–5 Jun, Rishabh 13–14 Jun, founders review 21 Jun.

---

## Key Discussion

### Pilot scope reconfirmation

Dan recapped the deliverables: Whimsical map of current operations, 4x structured context folders (one per person), group Claude Code setup session, and a Phase 1 prioritisation output. Rishabh confirmed the underlying goal: reduce people-dependency, standardise through SOPs, add AI to get capacity at ~120% of current cost but 200% of output. Dan's framing matched — the pilot is a discovery and mapping exercise, not yet building anything.

### Folder architecture shift

Rishabh pushed beyond 4 individual folders. He wants the deliverable to include a company-level folder structure with access tiers — departments can access their own subfolder, founders have full visibility. He explicitly asked for help architecting this, not just populating it. Dan accepted the scope addition. Rohit's folder inclusion is TBC — Rishabh to decide before sessions start.

### GitHub as distributed context host

Chandika and Rohit don't have company laptops — personal devices only. Hosting on individual Obsidian vaults doesn't work at scale. Dan pivoted: one GitHub repo as the company context layer, department subfolders with access levels, accessible from any device. No special software required for team members. This also gives version control.

### Pre-session context prep

Dan asked Growify to share existing docs ASAP — Rishabh's WorkFlowy (process/org thinking), Disha's org chart and structural docs, any SOPs. Rishabh asked Dan to send a written list of what he needs so they can prepare properly rather than guessing. Disha added a firm requirement: anything finalised for operations or tools must have both co-founders aligned — not just Rishabh's sign-off. This applies to process decisions and tool choices throughout the engagement.

### Session schedule

Rishabh away 30 May–9 Jun. Disha away 21 Jun–5 Jul. Growify end-of-season sale 27 May–15 Jun — team will be stretched.

Final schedule:
- **31 May** — Disha, 1h (first session)
- **4–5 Jun** — Chandika and Rohit, 2h each
- **6 Jun** — Disha, 1h (follow-up / gap fill)
- **13–14 Jun** — Rishabh, 1h
- **21 Jun** — Founders review, 2h (present map + folder structure + align on Phase 2 priorities)

The 21 Jun call is founders only — Rishabh explicitly said the team should not be in that call until founders are 70–80% aligned on findings.

### Model-independence framing

Dan positioned the context architecture as LLM-agnostic: the folder structure stays with Growify regardless of which model they use. Rishabh connected with this immediately — the goal was never to depend on any single provider. Dan outlined the long-term arc: start with high API usage → workflows mature → shift toward local models + deterministic scripts → lower token cost and zero vendor dependency within ~12 months.

---

## Action Items

| Owner | Action | By |
|-------|--------|----|
| Daniel | Send written context request list to Rishabh & Disha (WorkFlowy, org chart, SOPs, process docs) | ASAP — end of 25 May |
| Daniel | Send calendar invites: Disha 31 May (1h), Chandika 4 Jun (2h), Rohit 5 Jun (2h), Disha 6 Jun (1h), Rishabh 13–14 Jun (1h), Founders 21 Jun (2h) | This week |
| Rishabh | Share WorkFlowy and process/org context with Daniel | By 30 May |
| Disha | Share org chart and structural docs with Daniel | By 30 May |
| Rishabh | Decide on Rohit folder inclusion and inform Daniel | Before sessions |
| Disha | Brief Chandika & Rohit; confirm Jun 4–5 availability | Before sessions |

---

## Content & IP

### Post Material

- The model-independence pitch: clients don't realise they're locked into their AI vendor until they already are. Building the context layer first breaks that dependency before it forms — the structure is yours, the AI is interchangeable.
- The design workflow example: most people frame AI as replacing the designer. The real win is giving the designer something better to start from — transcript goes in, structured design brief comes out, human improves it. AI plus expert, not AI instead of expert.
- Disha's "both founders must say yes" rule is a sign of a healthy co-founder dynamic, not a blocker. Design the engagement to include her even when Rishabh is driving — decisions made unilaterally will stall later.

### Frameworks & Concepts

- **LLM-Agnostic Context Architecture** — structuring company knowledge in a portable, model-neutral format so the business is not dependent on any single AI provider. The context layer is yours; the AI is a utility plugged into it. Related to Folder-First Philosophy but the distinct value is vendor independence, not just ownership.
- **The Local LLM Progression Path** — planned arc over ~12 months: high API usage (workflows being built) → local models + deterministic scripts (workflows mature) → lower token cost and zero vendor dependency. Framed as the natural maturation of any well-built AI stack.

### Coaching & Advisory Patterns

- Pre-session context dump as a discovery technique: ask clients to share existing docs (WorkFlowy, org chart, SOPs) before the sessions. Cuts time spent on basics, lets extraction sessions go deeper faster.
- With co-founder clients, always confirm the decision-making protocol early. Who can say yes unilaterally? What requires alignment from both? Disha surfaced this explicitly — it's worth asking in every multi-stakeholder engagement.
