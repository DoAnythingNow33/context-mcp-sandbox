---
title: Jamie Cameron — Session 2
type: meeting
date: 2026-05-15
attendees:
  - Daniel (DoAnythingNow)
  - Jamie Cameron
status: complete
---

← [[entities/people/jamie-cameron]] | [[calendar/2026/Q2/may-2026]]

# Jamie Cameron — Session 2 — 15 May 2026

## Summary

Completed the Gmail MCP setup that was blocked after session 1 — OAuth credentials, Google Cloud consent screen, test user auth — and got the morning research report skill live and sending to Jamie's inbox. The report pulled real LinkedIn authors writing about enterprise AI with source links, no hallucination. Content pipeline discussion: once Jamie finds posts to emulate and writes an intent/audience file, the system will draft posts using writing DNA + audience context + meeting extracts. Next milestone is scheduled agents so the report runs at 8am without the terminal open. Agreed to do an in-person session to map Jamie's full workflow and build his unified context folder.

---

## Key Discussion

### Gmail MCP — Getting It Live

The bulk of the session was hands-on setup: Google Cloud project creation, enabling the Gmail API, building OAuth credentials, setting up the consent screen, adding Jamie as a test user, authenticating through the browser, and running the first test report. The process was fiddly (Chrome lag, OAuth consent screen steps, the token needing a test user added before it would authorise), but Claude troubleshot each wall. Jamie's pattern — paste error into Claude, follow the next instruction — held up throughout. Authentication successful. Email landed.

### Content Pipeline — What's Still Missing

Dan explained the full pipeline: writing DNA (from Jamie's existing posts) + intent/audience file (who you're writing for) + meeting extracts → LinkedIn draft. Jamie hasn't found the ToV posts yet (carry-forward from session 1). Dan demonstrated adding the audience/intent layer — it means the post draft isn't just tone-matched, it's audience-targeted. Dan committed to send a template.

### Unified Context Folder

Dan made the case for building Jamie a single folder that holds everything — clients, sessions, skills, transcripts. Jamie is currently running across three emails and multiple businesses (Cape Creative, Social Trait, ROI). Dan wants to understand the cognitive load in a dedicated session — what a day looks like, where the switching happens — so he can connect the right things. Agreed to do this in person.

### Scheduled Agents — Next Step

Once the email report is confirmed working, the next build is moving it from terminal-run to a scheduled agent on the Anthropic cloud — same logic, no terminal required, runs at 8am daily. Dan flagged this as the natural next step before the in-person session.

---

## Action Items

| Owner | Action | By |
|-------|--------|-----|
| Jamie | Find LinkedIn posts to emulate for writing DNA | Before session 3 |
| Jamie | Write intent/audience file (who you're targeting with content) | Before session 3 |
| Daniel | Send Jamie intent/audience file template | ASAP |
| Daniel | Schedule in-person session to map Jamie's workflows + build unified context folder | ASAP |
| Jamie | Confirm morning report email is landing daily | This week |

---

## Content & IP

### Post Material
- Non-technical users navigating AI setup: the real unlock isn't understanding — it's having a loop (hit wall → paste into Claude → follow instruction → repeat). Jamie said "I think if I just keep doing this with you weekly, I'll start to be able to do these things." That's the actual skill transfer — not knowledge, a *reflex*.
- "You, me, and Claude" — when Jamie said this after authentication succeeded, it signalled something real: non-technical users form trust with AI through *successful completion of hard things together*, not through explanation.
- The unified context folder pitch: most people's AI frustration comes from context-switching. The folder isn't a productivity hack — it's a memory prosthetic. Dan: "the best use I've got out of everything is that it knows all the moving parts."

### Frameworks & Concepts
- Copy-Into-Claude Loop — a troubleshooting technique for non-technical AI users: when you hit a wall, paste the error or screen into Claude and follow the next instruction. Bypasses the need to understand the error; builds confidence through forward motion.
- Scheduled Agents — same workflow logic as a local terminal run, but hosted on Anthropic cloud and triggered on a cron schedule. Makes automation durable and terminal-independent.

### Coaching & Advisory Patterns
- Jamie learns through demos and forward motion, not explanation. Session 2 confirms: he follows instructions under pressure, adapts when things break, doesn't need to understand before proceeding. The risk is he builds without understanding the architecture — fine for now, matters when he needs to debug alone.
- The in-person session matters more than it sounds: Jamie's workflow is genuinely complex (3 businesses, 3 emails, shifting project types day to day). He can't fully articulate it on a call. Getting it out of his head and onto paper is a precondition for building anything coherent for him.
