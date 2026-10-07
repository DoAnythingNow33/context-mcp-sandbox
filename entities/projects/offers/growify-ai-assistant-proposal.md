---
description: Growify Phase 2 proposal — always-on AI assistant for Rishab, built on his own context folder, presented 2026-07-29
type: profile
last_updated: 2026-07-28
---

# Growify — AI Assistant Proposal (for 2026-07-29 catch-up call)

Phase 2 of the Growify engagement. Phase 1 (ontology + context folder) is what makes this possible — this is the payoff Rishab has been building toward since the 2026-06-29 session, where the Hermes demo already landed well and he was bought in on voice-note capture.

## What Rishab Gets

An always-on AI assistant, reachable in Discord, that:

- Reads his Growify context folder as its source of truth — the same folder Dan has been building with him (shared Growify/Lookify context + Rishab's own self-folder)
- Captures voice notes and text on the spot and routes them to the right place (no manual filing)
- Knows his brand/team data from Airtable and his company brain from Workflowy, without him having to re-explain either
- Runs on Dan's own infrastructure (Hetzner), same pattern as Dan's personal Hermes — proven, not experimental

**Positioning:** this is not a chatbot bolted onto a folder. It's the same architecture Dan runs for himself daily — Growify is the first client proof of it working for someone else. It also anchors the next architecture step Dan is already building toward (context folder as the hub, Hermes executing directly in Airtable/Notion/Gmail per client) — Rishab becomes the first real test of that shift, not a one-off build.

## Structure — Two Phases

**Phase 1 (in progress):** Shared Growify/Lookify context folder + Rishab's self-folder. Ontology sessions, Airtable/Workflowy migration into folder structure.

**Phase 2 (this proposal):** The always-on assistant layered on top.
- Week 1: Discord bot live, reading his context folder, voice-note capture working
- Week 2+: Airtable connection deepens from manual export to a live pull (brand/team data updates flow into the folder automatically)
- Ongoing: Dan on call for anything that needs adjusting — model behaviour, routing rules, new data sources

## Pricing

£500/month, no separate setup fee — the setup is covered by the existing £750 Growify Phase 1 fee (paid on delivery of the ontology, which Dan is finishing now). Positioned as roughly a tenth the cost of a human PA (£40–60k/year UK), and framed as additive: it's not replacing a human assistant, it's the layer that catches the 2am ideas and the voice notes that would otherwise go nowhere.

## What Dan Needs From Rishab Tomorrow (or right after)

1. Confirm which Discord account he'll use, and enable Developer Mode → get his Discord User ID
2. Generate an Airtable Personal Access Token, scoped to the client-management base (read-only to start) — instructions: airtable.com/create/tokens
3. Sign-off on £500/month for Phase 2 — no setup fee, since that's covered by the £750 Phase 1 fee due on ontology delivery
4. Confirm timing for the joint Rishab + Disha session (still unscheduled) — Disha's instance follows once she's replied and had her own self-folder session

## Live Demo Plan for the Call

1. Show Dan's own Hermes responding in Discord — voice note in, routed correctly, "this is what you're getting"
2. Walk through his own context folder structure (already partly migrated) — how the assistant reads it
3. If the Discord bot is live by then (see `hermes/multi-tenant-setup-sop.md`): have Rishab send it a real message live on the call
4. Close on the two-phase structure and pricing above; get a yes/no on Phase 2 timing

## Open Questions Carried Over

- Exact ongoing Airtable sync mechanism (manual export now, live pull script next — see SOP §5)
- Whether Rishab wants to fund his own OpenRouter usage separately or fold it into the £500/month
- Phase 1 fee (£750) still due on ontology delivery — Dan finishing that now; frame Phase 2 as already-covered setup, not a new ask

## Related

- [[../../hermes/multi-tenant-setup-sop]] — technical build steps
- [[../../entities/people/growify]] — full entity snapshot
- [[../../meetings/2026-06-29-growify-session-2]] — where this offer model crystallised
- [[ai-workflows]] — the parent offer this instantiates
