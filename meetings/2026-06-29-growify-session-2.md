---
title: Growify — Session 2
type: meeting
date: 2026-06-29
attendees:
  - Daniel (DoAnythingNow)
  - Rishab Mehra (Growify)
status: complete
---

← [[entities/people/growify]] | [[calendar/2026/Q2/june-2026]]

# Growify — Session 2 — 29 June 2026

## Summary

Rishab walked Dan through his full tool stack: Workflowy (company brain + pipelines), Airtable (brand/team management), Arc (browser spaces organised by company), and a local folder structure mirrored to Google Drive. The conversation produced a clear scope decision — drop Chandika and Rohit for now and focus the pilot entirely on Rishab and Disha sharing one Growify/Lookify context folder, each with their own self-folder alongside it. Rishab will share Workflowy exports (Growify node + teams node) and an updated Airtable client sheet tomorrow; Dan migrates them into the folder structure. Hermes demo landed well — Rishab understood the folder-to-agent bridge and is bought in on voice-note capture. Dan's offer model crystallised through the conversation: AI personal assistant, £1k setup + £500/month, positioned as a tenth the cost of a human PA — Growify is the proof of concept.

<!-- TODO(client-sync): push summary to Notion client portal when integration is built -->

---

## Key Discussion

### Rishab's current tool stack

Workflowy holds the company brain: growify plan, teams structure, SOPs-to-be-built, AI workflows per department. Nodes are organised as dropdown + Kanban (left-to-right board within a dropdown). Airtable holds the live brand/team data — which brands each team manages, Facebook and Google managers, POC per brand, incentive structure. Arc browser has spaces per company (Growify, Lookify, Engage/Quota, Aap Ka Awaas, and a catch-all for side ideas). A local document folder, partially mirrored to Google Drive, holds dashboards vibe-coded earlier and master prompts. Rishab also described internal AI tools in progress: Rossify (identifies underspent high-potential products), a price tracker across sites, Craftify (adds design templates to Shopify product images for Meta ads), and Funnel — a middleware connecting Shopify, Facebook, and Google data, with an MCP endpoint being wired to Claude for funnel analysis queries.

### Scope decision: founders first

Chandika and Rohit are out for now. The pilot is Rishab + Disha sharing one folder (Growify + Lookify in scope) with individual self-folders sitting alongside the shared business context. The rationale: no permissions complexity, both founders have full access, and proving value at this level is the prerequisite for extending to senior management. Lookify comes in alongside Growify because they are operationally the same entity — same founders, same team.

### Shared folder architecture + self-folders

The business context folder is the shared source of truth — both founders pull from and contribute to it, so each person's AI agent has the same underlying context without needing to be in the same tool. Separately, each founder gets their own self-folder (beliefs, goals, identity, arc) so any AI agent knows them as a person, not just as operators of the business. This also enables the Reality Architect Coach to run against the self-folder independently.

### Hermes as the capture bridge

Dan demoed Hermes — the always-on assistant with SSH access to the GitHub-synced folder. Rishab's described desire (voice recordings that auto-route into the right place) maps exactly onto this setup. Key design point surfaced: Hermes is intentionally kept light — personality and memory of the user only — with the heavy context in the folder. The routing layer (CLAUDE.md + context files) means Hermes navigates to the right file without reading everything, which keeps token use minimal and responses fast.

### Dan's AI PA offer model

The conversation crystallised Dan's positioning: AI personal assistant as a service. £1k setup, £500/month maintenance, Dan on call. Compared to a human PA at £40–60k/year (UK), this is roughly 1/10th the cost. The framing: it's not replacing the human assistant — it's adding a layer between the founder and the assistant (and handling the 2am ideas the founder shouldn't text a person about). Growify is the proof of concept that will let Dan structure onboarding into a clear step-by-step process.

### Airtable and Workflowy sync

Rishab asked about syncing live data (Airtable, Workflowy) into the folder. Workflowy has an MCP. Dan flagged the risk of importing noise along with signal — preference is to filter manually first, then automate once the clean structure is established. Airtable client sheet will be updated by Rishab and sent tomorrow; Dan will handle the migration and figure out the ongoing sync approach.

---

## Action Items

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | Update Airtable client sheet and send to Dan | Rishab | 2026-06-30 |
| 2 | Share Workflowy exports: Growify node + teams node | Rishab | 2026-06-30 |
| 3 | Review Workflowy + Airtable exports and migrate into folder structure | Dan | TBC |
| 4 | Build self-folder structure for Rishab (and template for Disha) | Dan | TBC |
| 5 | Set up Hermes pipeline for Rishab (Telegram or Discord) | Dan | TBC |
