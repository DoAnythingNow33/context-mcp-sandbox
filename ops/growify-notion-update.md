---
title: Growify-Rishab Notion Client Portal Update
date: 2026-08-18
status: ready_to_sync
---

# Growify-Rishab Notion Client Portal — Meeting Summary Update

Based on a pull from GitHub (latest: commit 6f75165 + 7 days of nightly health evals), here is everything missing from the Notion client portal. All meeting summaries are current as of 2026-07-30.

---

## Summary for Rishab

**Relationship:** Growify (e-commerce/Shopify agency, ~110 people) — Phase 1 ontology + AI assistant delivery engagement  
**Status:** Phase 1 delivery complete; Phase 2 proposal ready  
**Last updated vault:** 2026-07-30  

---

## Meetings Completed (Chronological)

### 1. **Call — 24 May 2026**
- **Attendees:** Daniel, Rishabh, Disha
- **Outcome:** Locked Phase 1 scope and session schedule
- **Key decisions:**
  - Pilot scope: Whimsical map, 4x structured context folders, group Claude Code setup, Phase 1 prioritisation
  - Architecture shift: company-level folder (not just individual) with access tiers
  - Hosting: GitHub (not Obsidian local) so Chandika/Rohit can access from personal devices
  - Session schedule locked around travel: Disha 31 May + 6 Jun, Chandika/Rohit 4–5 Jun, Rishabh 13–14 Jun, founders review 21 Jun
  - Model-independence framing: context layer is vendor-neutral; AI is interchangeable

### 2. **Brain Dump — 5 June 2026 (Disha)**
- **Attendees:** Disha (Founder, Ops), Daniel
- **Type:** Full ontology extraction session
- **Outcome:** Complete company structure and process documentation
- **What surfaced:**
  - **Team structure:** 4 teams (~18 brands each, ~10 people per team) + Website team + Imagery Sizing team
  - **Clients:** ~60 total (40 live at time of session); tiered Top/High/Medium/Low
  - **Revenue model:** Incentive-based (% of client revenue)
  - **Seven core processes:** Creative (image resizing + ad design), Reporting, Performance tracking ("brands in red"), Client onboarding, Client escalation, Employee onboarding, Employee exit
  - **Biggest problems identified:**
    1. Knowledge concentrated in Disha (single point of failure)
    2. Creative bottleneck: need 20 campaigns/day, delivering 9–10/day
    3. Image resizing: 5-day, 3-resource manual cycle per upload
    4. Reporting overload: ~20 manual weekly reports at 1.5–2 hours each
    5. Client expectation mismatches (Rishabh's BD promises not documented)
    6. No defined, fast escalation path
  - **Proposed architecture:** PostHog (analytics) + Claude (workflows) + GitHub (context) + role-specific dashboards

### 3. **Ontology & Meeting Summary — 5 June 2026 (Disha)**
- **Type:** Structured notes from Session 2 above
- **Deliverable:** Full ontology map with actors, clients, teams, systems, processes, problems, and proposed architecture

### 4. **Session 1 (Rishab) — 13 June 2026**
- **Attendees:** Daniel, Rishabh
- **Duration:** 1 hour
- **Outcome:** Architecture alignment and data infrastructure clarity
- **Key insights:**
  - Rishab is fluent in second-brain concepts (watches Claude/Obsidian videos, understands token logic)
  - **Current data stack:** Workflowy (company brain) + Airtable (brand/team live data) + Arc (browser spaces) + Google Drive (local docs) + custom Funnel middleware
  - **Three-layer architecture agreed:**
    1. **Context folder (Obsidian)** — lightweight, local, workflow-first; holds brand strategy, team context, company workflows
    2. **PostHog** — analytics and data layer; AI-queryable; replaces fragile Power BI setup
    3. **Notion** — client-facing portal; syncs from context folder via Python/Claude/Notion MCP hook
  - **Key value insight:** As brand knowledge accumulates, switching costs compound — context folder becomes a retention mechanism
  - **Secondary benefit:** 60+ brands = pattern intelligence; queryable cross-client data becomes a consulting asset
  - **Action:** Rishab to review PostHog vs current Power BI; map brand-level context requirements; confirm Zoho migration timeline (People + CRM + Books)

### 5. **Session 2 (Rishab) — 29 June 2026**
- **Attendees:** Daniel, Rishabh
- **Duration:** ~1.5 hours
- **Outcome:** Tool stack clarity, scope decision, and AI PA positioning crystallised
- **Key discussion:**
  - **Rishab's live tool stack:** Workflowy (company brain + pipelines via dropdown/Kanban), Airtable (live brand/team data), Arc (browser spaces per company), local folder (dashboards + master prompts); internal tools in progress: Rossify, price tracker, Craftify, Funnel
  - **Scope decision:** Drop Chandika/Rohit for now; pilot is Rishab + Disha sharing one Growify/Lookify folder with individual self-folders alongside
  - **Shared folder architecture:** Business context folder (shared source of truth) + individual self-folders (beliefs, goals, identity, arc) so any AI agent knows both the business and the person
  - **Hermes demo landed:** Rishab understood the folder-to-agent bridge; bought in on voice-note capture
  - **AI PA offer model crystallised:** £1k setup + £500/month maintenance (roughly 1/10th cost of human PA at £40–60k/year); positioned as a layer between founder and assistant
  - **Airtable/Workflowy sync question:** Risk of importing noise — preference is manual filter first, then automate once clean structure established
  - **Action:** Rishab to send updated Airtable client sheet + Workflowy exports by 2026-06-30

---

## Current Status (as of 2026-07-30)

### Phase 1 Completion
- ✅ Disha session (31 May)
- ✅ Chandika session (4 Jun)
- ✅ Rohit session (5 Jun)
- ✅ Disha follow-up (6 Jun)
- ✅ Rishabh session (13 Jun)
- ✅ Rishab session 2 (29 Jun)
- ✅ Rishab catch-up call (29 Jul) — confirmed Phase 1 complete
- ✅ **Growify Assistant shipped 2026-07-29** — fully functional always-on Hermes instance, reading real Growify context folder (private GitHub repo `growify-context`), dedicated Linux user, separate OpenRouter billing

### Outstanding Items
- **Disha's self-folder session** — promised as part of Phase 1 scope; still pending her reply (no response since 2026-07-11)
- **Chandika + Rohit individual sessions** — were part of original Phase 1 scope but narrowed to founders only; decision: postpone until Phase 2 is approved
- **Notion client portal build** — Growify Assistant is reading context, but client-facing Notion sync not yet wired (pending Dan's NOTION_TOKEN setup)

### Phase 2 Status
- **Proposal drafted & ready:** `entities/projects/offers/growify-ai-assistant-proposal.md`
- **Positioning:** The Growify Assistant build is the proof of concept for Dan's "AI PA" offer model
- **Next step:** Present Phase 2 proposal to Rishab (pending this meeting with you)

---

## What to Update in Notion

### For Rishab's View

**Completed work:**
1. ✅ Disha ontology session (31 May) — full extraction + map + process architecture
2. ✅ Chandika session (4 Jun) — brand management context + folder architecture input
3. ✅ Rohit session (5 Jun) — operations context + performance tracking system
4. ✅ Rishabh session 1 (13 Jun) — data infrastructure + 3-layer architecture alignment
5. ✅ Rishabh session 2 (29 Jun) — tool stack clarity + scope decision (founders-only pilot) + AI PA offer positioning
6. ✅ Growify Assistant shipped (29 Jul) — fully functional, live, reading context folder

**Outstanding:**
- Disha's individual self-folder session (TBC — awaiting her reply)
- Phase 2 proposal review (ready to present)

**Key insights logged:**
- Switching cost mechanism: accumulated context = retention
- Cross-client pattern intelligence as a consulting asset
- AI PA positioning: £1k setup + £500/month (1/10th cost of human PA)
- Shared folder + self-folder architecture for both business context and personal identity

---

## Files to Reference

All meeting summaries + entity state live in:
- **Client state:** `/entities/people/growify.md` (last updated 2026-07-30)
- **Meeting files:**
  - `meetings/2026-05-24-growify-call.md`
  - `meetings/2026-06-05-growify-ontology.md` (detailed)
  - `meetings/2026-06-05-growify-brain-dump.md`
  - `meetings/2026-06-13-growify-session-1.md`
  - `meetings/2026-06-29-growify-session-2.md`
- **Phase 2 proposal:** `entities/projects/offers/growify-ai-assistant-proposal.md`

---

## How to Update Notion

**If Notion sync is live:** Run the sync script to auto-push all meeting metadata + current state to the client portal.

**If manual:** Copy the "Completed work" and "Outstanding" sections above into Rishab's Notion record under "Engagement history" or "Session log."

**Suggested Notion structure for client portal:**
- **Status card:** Phase 1 complete, Phase 2 ready to discuss
- **Timeline:** Sessions completed (with dates); Growify Assistant live since 2026-07-29
- **Key outcomes:** 3-layer architecture, switched to founders-only scope, AI PA offer positioning
- **Next steps:** Phase 2 proposal discussion (this meeting)
- **Link to docs:** Context folder (private repo), meeting notes (shared when appropriate)

---

**Updated:** 2026-08-18 (from latest vault pull)  
**Next sync:** After your meeting with Rishab today
