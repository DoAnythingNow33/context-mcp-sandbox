---
description: Current active threads — what's being worked on right now, updated every week
type: profile
last_updated: 2026-07-28
---

# Goals

Current active threads. Updated at the end of every weekly planning session. This is the orientation file — tells a fresh session what matters right now.

## Active Threads

- **Long game to freedom, not a grind against a deadline — resolved 2026-07-08.** ~£12,000 saved + new job (delivery driver for Ottolenghi's CPU, ~£1,200/month, replacing Farmer J from 2026-07-09) covers the near-term floor; no hard deadline to hit £5k/month before the baby (due end of August). Since then Dan has taken ~3 weeks off the business for house prep for baby #2 and family time — this session (2026-07-28) is catching the vault back up.
- **Notion/Airtable execution layer — new 2026-07-28, target ~2026-08-11, first win 2026-08-14.** Extends the in-progress Notion client-portal sync (`docs/DEFERRED.md` §1) into a full architecture shift: the context folder becomes a pure hub (meetings, notes, instructions), Hermes reads it and executes the real operational work per client inside Notion, Airtable, or Gmail (chosen per client) rather than the context folder itself holding operational data. 2026-08-14: full vault audit run — fixed stale README.md and a hermes-capture.md routing contradiction, migrated the 51-prospect CRM from vault markdown to a Notion database (`ops/sales/` now docs-only, CRM lives in Notion), reorganized `visual/`. `ops/notion-index/` (2,779-page triage) still pending. Broader per-client execution layer still to scope.
- **Growify delivery** — Phase 1 still in progress; Rishab S1 done, PostHog shared; Chandika + Rohit sessions outstanding, plus one more each with founders; Phase 2 proposal follows close. Rishab catch-up call held 2026-07-29; the always-on Hermes assistant ("Growify Assistant") was built and shipped that same day, then consolidated to `claude-sonnet-5` on both model slots 2026-07-29/30 (matching Dan's own instance). Disha still hasn't replied, her self-folder session remains un-held.
- **AI Workflows outreach** — 50 prospects loaded; 10 sent WC 16 Jun; goal: complete list + follow up on 10 this week; AI Clarity Call (free, 30 mins) → Context Folder Build (£500/day)
- **Identity reframe — resolved 2026-07-08.** Worked out the unified brand architecture with coach today. **DoAnythingNow.** is the whole: mission is helping humans remember the magic of being human again, creativity as the superpower in all aspects of life. Two arms under it — **MakeWorkFlow** (AI workflows: AI does the robotic work so humans can do the creative work they're uniquely able to do) and **Reality Architects** (coaching/framework arm; one-liner, final, my own words: "Reality is not fixed, you create yours. Every meaning you define, every decision you make bends the timeline you're on in real time."). Next: articulate this on the website — 3 landing pages (AI Workflows/MakeWorkFlow, Reality Architects, Hub) — deferred, not urgent, focus elsewhere for now.
- **Content engine — unblocked 2026-07-13.** Identity sentence resolved: "DoAnythingNow helps humans remember the magic of being human again — creativity as the superpower in every part of life." (→ `self/identity.md`.) LinkedIn and Instagram had slipped 3+ weeks on identity confusion; that root cause is gone. Next: produce again — Sleevenote, carousel, and website next_actions that were gated on this sentence are now filed to `actions/backlog/`.
- **Carousel content system** — building framework + templates for consistent carousel production (educational, narrative, announcement). Live alongside main content engine.
- **Sleevenote opportunity** — partnership to be community leader & strategist on tiny audio product team. First video completed. Current priority: get the 3D-printed clip accessory case actually made (design + manufacturing). Vision: organic adoption via key taste-setters. Cooling as of 2026-08-11 — Tom passed on the Soho Spirits Festival opportunity and has been dismissive of hardware/market research Dan's sent over; watch whether this is still worth investing time in.
- **Victoria Russel / Mycelium partnership — new 2026-08-11.** Dan and Victoria explicitly agreed to work together going forward: regular syncs, an introduction/consultancy-fee model connecting each other's networks to opportunities, self-funding Victoria's broader Mycelium concept (privatising creativity, multidisciplinary private investment). Next: formalize the fee structure in writing.
- **Skilljar certificates** — 2 of 5 done; get 3 more
- **Sam / Explorers Club** — still no reply from Sam on scheduling the catch-up call, as of 2026-07-28
- **Shereen / Bubble Balloon Heaven** — deposit finally sent; build now in progress, working locally outside the vault
- **Fix the morning block** — sleeping by 10:30pm, waking by 6:30am consistently
- **Visual command centre** — background only
- **Ontology for Creatives (institutional partnerships) — new 2026-07-29.** Sparked by a conversation with a friend: many creatives need support/systems for a balanced life, and ontology is the right subject to deliver that at another level — working with institutions that engage creatives (e.g. Roundhouse) to run workshops. Early/felt-direction stage, not yet scoped. See `entities/projects/ontology-for-creatives.md`.

## Business Threads

Two-track model (decided 2026-06-12):
- **AI Workflows consulting** — primary income engine now; AI Clarity Call → Context Folder Build (£500/day); grind outreach to fund the transition
- **Reality Architects coaching** — long game; content, community, Skool compound slowly; not pressured to pay rent

Previous three-pillar structure:
1. **Coaching** — content engine running; funnel pointing toward Skool and 1:1; "Concepts with Dan" series started
2. **Ontology / AI Systems** — Growify proof of concept; methodology replicable
3. **Skool community** — free community, upsell to 1:1; keep promoting

Creative arm: Santiago/Bonita — archived 2026-07-13, gone quiet for 2+ months, no active work.

→ [[entities/projects/snapshot]]

## Family Threads

- Baby due end of August 2026 — runway must be built before then
- Son (2 years old) — family dinner 6pm, bed by 8pm, protected routine
- Partner — evenings protected, wind-down time is not negotiable
- Farmer J part-time — ends 2026-07-09 (Thursday, last day); replaced by delivery driver work for Ottolenghi's CPU (central production unit) (Sat–Mon, 6am–1pm, ~£1,200/month, 4 days off) as the financial floor

→ [[entities/people/family]]

## Personal / Arc Threads

- Morning discipline — sleep earlier, protect the 6:30–11:30am block
- Finish before starting the next thing — sequencing, not multitasking
- Living the frameworks (ontology / psychology / embodiment) in own life, not just with clients

→ [[self/arc]]

## Someday / Deferred

- Hire home manager and cook — as income grows, to free time and energy
- Relocate to Spain or Italy (~2027/28) — new build, slower pace, London for summers

## Completed

- 2026-08-13: Victoria Russel client card + portal built in the Notion CRM (off the Growify template); vault catch-up DPL + both Victoria meetings processed after a 2-week gap
- 2026-07-30: Hermes model consolidation — Dan's own instance confirmed on `claude-sonnet-5` (Anthropic direct); Growify's instance collapsed from a Haiku/Sonnet split to `claude-sonnet-5` on both slots (OpenRouter); found + fixed a duplicate-Discord-reply bug caused by a stray local `launchd` gateway on Dan's Mac
- 2026-07-30: Jamie/Dan joint pitch deck built + deployed live (jamie-pitch.vercel.app) — "The Notion Manager," using the Growify build as proof-of-concept case study
- 2026-07-08: Quit Farmer J — last day 2026-07-09 (Thursday); replaced by delivery driver work for Ottolenghi's CPU (Sat–Mon, 6am–1pm, ~£1,200/month, 4 days off) as the financial floor
- 2026-07-03: Hermes migrated fully to Discord — dedicated channel, morning/evening debriefs fixed, TTS live (Edge TTS), Claude Code CLI set up on the Hetzner server
- 2026-07-03: 3D HTML DoAnythingNow logo built for the new website
- 2026-07-03: Family finance tracker fixed — Notion migration next
- 2026-05-18: Skool community fully complete — all modules live, Module 0 redone for consistency
- 2026-05-18: Growify invoice sent — 50/50 structure confirmed
- 2026-05-12: Concepts with Dan ep 2 posted
- 2026-04-04: Context system initialised
- 2026-04-09: Self layer baseline written
- 2026-04-13: Lead magnet created
- 2026-04-22: Santiago equity formalised — make Bonita profitable, equity in return
- 2026-04-26: Growify scope aligned — founders-first pilot agreed
- 2026-04-27: Funnel confirmed — lead magnet → Skool or 1:1
- 2026-04-27: Lead magnets fully live on Stan store (free + £5, cleanly distinguished)
- 2026-04-27: Applied for Google Creative Lives in Progress AI prompting lab
- 2026-04-29: All Skool module content written
- 2026-04-29: Context system cleaned and simplified
- 2026-05-01: Skool Module 0 complete — video, audio (Adobe Podcast), article, welcome post pinned
- 2026-05-01: Skool community price raised — paid community live
- 2026-05-03: Timeline Maxxing Episode 4 posted
- 2026-05-03: Cluely application sent (name/age/location video)
- 2026-05-03: Invoices sent; Revolut invoice process confirmed — simple, keeping it
- 2026-05-04: Rishab/Disha teaching moments extracted (Growify call 2 file merged into new context)
- 2026-05-10: All Skool modules filmed; Module 1 edited and live
- 2026-05-10: Instagram reels posted Mon–Fri — consistent week
- 2026-05-10: Growify proposal accepted — first paying ontology/AI client confirmed
- 2026-05-10: Jamie BizDev session 1 done; £150/4-session deal agreed
- 2026-05-12: Skool module 2 edited and posted
- 2026-05-12: Skool module 3 edited and posted
- 2026-05-12: Concepts with Dan ep 2 recorded, edited, and posted
- 2026-05-15: Fadwa session 5 notes processed via /meeting
- 2026-05-21: Shereen / Bubble Balloon Heaven — web dev client converted from cold call, £250/5hrs
- 2026-05-24: Growify Phase 1 session schedule fully locked — 6 sessions, 31 May–21 Jun
- 2026-06-02: Website live
- 2026-06-02: Skool offer reshaped — free community, first group call 7 Jun
- 2026-06-02: Personal ontology fully built — methodology foundation in place
- 2026-06-05: Jamie final session complete — AI pulse report delivered (daily Gmail drafts), content engine live (report → LinkedIn/Twitter talking points), Obsidian vault + Base set up as content bank
- 2026-06-07: Skool first group call — no shows; continuing to promote
- 2026-06-12: Growify Disha session 1 done; Rishab session 1 booked for 2026-06-13
