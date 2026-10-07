---
title: Jamie Cameron — Session 1
type: meeting
date: 2026-05-08
attendees:
  - Daniel (DoAnythingNow)
  - Jamie Cameron (Cape Creative / Social Trait)
status: complete
---

← [[entities/people/jamie-cameron]] | [[calendar/2026/Q2/may-2026]]

# Jamie Cameron — Session 1 — 08 May 2026

## Summary

First paid session. Jamie works at Social Trait (AI personas/synthetic audiences tool) and is taking over their LinkedIn and X presence. He needs a pipeline from calls → content bank → posts and a daily research brief on enterprise AI. We installed Claude Code on his terminal, explained the skills-as-workflow architecture, started building a call extraction skill and content generation skill, and agreed the engagement structure: 4x Friday sessions in May at £150/session.

## Key Discussion

### Current State: Clay → HubSpot Lead Gen
Jamie's primary activity at Social Trait is outbound: generate leads in Clay, manually filter by role title and company type (consumer goods, retail), upload to HubSpot, send automated sequences with personalized emails (Claude-assisted), then hand-write directly when leads engage. He considers this workflow locked — no obvious efficiency gain — so we moved on.

### LinkedIn/X Engagement Strategy
Jamie is taking over Social Trait's LinkedIn and X accounts. Goal: get into conversations in the enterprise AI space, comment on high-engagement posts, and establish Social Trait's presence. He needs thought leaders, influencers, and communities to engage with. Reddit, Substack, Medium are scrapable; LinkedIn and X are anti-scraping, so a direct feed won't work there. The AI Pulse skill handles the research side.

### Claude Code Setup
Installed Claude Code on Jamie's terminal from scratch — including working through the capital-letter bug on folder drag-to-terminal. Explained why terminal > desktop app for workflow automation: it can run scripts and execute code directly, which the desktop app cannot. Demo'd the meal planner skill as a concrete example of the build-once, use-always pattern. Also flagged Opus usage limits — he was running Opus in a co-work thread and couldn't switch mid-thread; needs to use Sonnet by default.

### Skills-as-Workflow Architecture
Core mental model: each atomic step is a skill, a full workflow is a pipeline of skills. Jamie's content workflow maps to three skills:
1. `/call-extraction` — transcript in, content bank file out
2. Tone-of-voice extraction — finds and emulates existing LinkedIn posts, produces a template file
3. `/linkedin-posts` — content bank file + tone template in, LinkedIn-ready posts out

Jamie started building the call extraction skill in the terminal during the session. Folder structure created: `Claude SocialTrait/` with a `content-bank/` subfolder. Also discussed tracking processed files — a `processed/` subfolder so already-used content bank entries are clearly separated.

### AI Pulse Skill
Daniel built a skill during the session that runs every weekday at 8am, searches Reddit/Substack/Medium/public tweets for enterprise AI + synthetic audiences content, and delivers a curated email digest. Daniel will email Jamie the skill file post-session; Jamie installs it via terminal and sets up Gmail MCP. They'll review the first week's emails in session 2 and tweak if needed.

### Engagement Terms
Four Friday sessions in May, £150/session. This session counted as session 1 (originally a 2-hour session at £50/hour, renegotiated to 1-hour weekly at £150). After four weeks they'll reassess.

## Action Items

| Owner | Action | By |
|-------|--------|----|
| Daniel | Email Jamie AI Pulse skill + setup instructions; request Gmail MCP auth | ASAP |
| Daniel | Email Jamie call summary | ASAP |
| Jamie | Install Fathom for future call recording | Before session 2 |
| Jamie | Find 3–5 LinkedIn posts to emulate; run tone-of-voice extraction in terminal | Before session 2 |
| Jamie | Install AI Pulse skill via terminal, set up Gmail MCP, confirm first 8am report received | Before session 2 |

## Content & IP

### Post Material
- Most people think AI tools save time on the obvious tasks — the real unlock is when they remove the coordination overhead between steps (copy this → paste here → wait → now do that). Claude Code collapses that into one terminal command.
- "I've just realized I need another piece to the puzzle" — the moment mid-build when a missing dependency surfaces. That's not a failure of planning, that's the nature of workflow design: you can't see the full chain until you start building.
- The meal planner demo: trivial use case, genuinely useful output. The best way to explain Claude Code's value isn't the impressive thing — it's the embarrassingly practical thing that lands.

### Frameworks & Concepts
- **Skills-as-Workflow-Steps** — each atomic action is a skill, a full workflow is a pipeline of skills. You don't build one giant prompt; you build a chain of small skills, each with one job.
- **Content Pipeline from Calls** — structured technique: record call → extract transcript → run `/call-extraction` → content bank file → run `/linkedin-posts` → ready-to-edit drafts. Removes the blank-page problem for content creation entirely.

### Coaching & Advisory Patterns
- Jamie knows the tools exist but doesn't know how to chain them. The unlock isn't teaching individual tools — it's showing the architecture of a workflow and letting him fill in the steps himself.
- He's resistant to complexity until he sees a simple demo. The meal planner cracked it open — show the dumb, personal example first, then scale to the work use case. This pattern recurs: concreteness before abstraction.
