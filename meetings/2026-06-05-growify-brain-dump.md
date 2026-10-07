---
title: Growify — Brain Dump
type: meeting
date: 2026-06-05
attendees:
  - Daniel (DoAnythingNow)
  - Disha Bhatnagar
status: complete
---

← [[entities/people/growify]] | [[entities/people/disha]] | [[calendar/2026/Q2/june-2026]]

# Growify — Brain Dump — 05 June 2026

## Summary

Disha gave a full operational brain-dump on AI opportunities across Growify's internal workflows. Three hard bottlenecks surfaced with numbers: image resizing (1hr 15min per 5-image batch; need 20 campaigns/day, doing 9-10), ad creative production (same pipeline, same backlog), and weekly client reports (1.5–2hr per report × 20 clients/week). Architecture direction is clear: one shared Claude account company-wide with brand-specific context folders, PostHog to replace the custom analytics dashboard (currently 5 lakh/quarter), Claude-powered workflow automation for creative and reporting. Disha is sending raw images + specs + sample report; Daniel tests workflows and researches PostHog; Chandika and Rohit meetings to be booked separately to map the information architecture.

<!-- TODO(client-sync): push summary to Notion client portal when integration is built -->

---

## Key Discussion

### Internal AI infrastructure — the fragmentation problem

Every person at Growify is running their own ChatGPT or Claude account. Brand context is scattered across personal chats, floating TPTs, and Google Drive folders with no consistent structure. Rishabh, Disha, Chandika, and the marketing team are all generating context from different, unshared bases — producing inconsistent outputs and copy with no ability to train or improve. The fix is one shared company-wide account with permissions by role and a standardised context folder per brand. Daniel's approach: find one clean example brand, architect the folder structure with Chandika, then roll it out as a template all brand managers replicate.

### Image resizing — highest-effort, lowest-value bottleneck

Process: client sends WeTransfer → team downloads and re-uploads to Drive → resizing team manually adjusts each image (uniform headspace, margins, dimensions) → re-uploads → website team downloads and publishes. Five images per campaign. Currently taking 1hr 15min per campaign, with a daily requirement of 20 and actual throughput of 9-10 — permanently backlogged. Daniel's assessment: this is solvable with the same approach he used for video (automated clipping via timestamp) — uniform headspace/margin rules + automation should handle it. Disha to send 5 raw images + resizing specs; Daniel builds a test workflow.

### Ad creative generation — same backlog, different cause

Designers are spending 20 min on templates and another 55 min on placement, font experimentation, and pixel-perfect adjustments for each campaign. The actual creative brief is simple: image + logo + sale text or collection name. Brand books already define font and placement rules. The fix is a tool where designers upload the image, select the brand, choose placement orientation (top/bottom/left/right), and publish — removing all the experimentation and drag/drop time. Adobe Firefly may already cover this within Photoshop; Daniel to test rather than switching tools.

### Reporting — the heaviest manual burden

Growify uses a Funnel-powered dashboard aggregating Meta, Google, and Shopify data in real time. Clients can't interpret raw numbers — they want signal: what's working, what isn't, what's being fixed. Despite the dashboard existing, every team member manually screenshots data, builds a PPT, adds written insights, and sends it — then revises based on feedback. That's 1.5–2hr per report × 20 clients/week × one resource each. Daniel's recommendation: connect the reporting data to Claude with a templated output format (Disha to send one clean example report); separately evaluate PostHog as a replacement for the custom dashboard tool to reduce the 5 lakh/quarter spend.

### Process mapping — onboarding and escalation gaps

Onboarding gap: Rishabh closes deals solo, committing things verbally that aren't documented or communicated to the ops team. When onboarding happens (without Rishabh), expectations don't match what was promised. No accountability trail exists. Disha's solution: whatever Rishabh promises on a closure call needs to be recorded and sent to someone — transcript, note, anything.

Escalation gap: Disha described a four-stage escalation model she's designing — brand manager flags (2 months below target) → team lead dip-check call → CSM strategy intervention (fancy plan, 1-2 months to implement) → Disha/senior team join. Currently escalation comes straight to Disha because there's no defined process. The system is in her head; it needs to be documented and automated (flagging brands in red automatically rather than waiting for a manual Friday WhatsApp update).

Internal reporting gap: Rohit built a colour-coded lookup (brands below 25% of target → red) that would automate the Friday status update. Rishabh wants the team to do it manually so they feel the underperformance. Disha sides with Rohit — automating detection is not the same as removing accountability; humans should be responding to the alert, not creating it.

### Architecture direction

One source of truth per layer: brand context in one Drive structure, analytics in one dashboard (PostHog candidate), escalation triggers automated not manual, role-specific views (POC, brand manager, team lead, Disha/Rohit) built on shared data. Daniel's framing: the humans do the human work; robots do the robot work. Adopting AI and continuing to manually generate data that could be automated is the worst outcome.

### Chandika and Rohit sessions

Both need separate sessions with Daniel — Chandika for information architecture (she holds the messy history of previous Drive structure attempts), Rohit for the reporting and escalation automation. Disha to forward Daniel's Notion booking link to both.

---

## Action Items

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | Send 5 raw images + resizing specs + ad brief + sample client report | Disha | This week |
| 2 | Test image resizing and ad creative workflows using Disha's assets | Daniel | This week |
| 3 | Research PostHog for analytics; report back to Disha | Daniel | This week |
| 4 | Send Notion availability link to Disha | Daniel | Today |
| 5 | Book sessions with Chandika and Rohit using Daniel's link | Disha | This week |
