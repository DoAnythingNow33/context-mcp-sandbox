---
description: "Meeting summary syncer — updates the entity file and the day's DPL from a meeting. Runs as Agent 2 inside /meeting, or standalone on any meeting file."
---

# /summary — Meeting Summary Syncer

Downstream sync for a meeting: updates the client or project entity file and appends to the day's DPL. Runs as Agent 2 inside `/meeting`, or standalone when Dan wants to sync a meeting file that wasn't processed through the full orchestrator.

---

## Mode detection

**Orchestrated (called by `/meeting`):** The meeting file path, entity name, entity type (people/projects), and meeting date are passed in. The base meeting file and its Summary section already exist. Focus entirely on the downstream sync — Steps 3 and 4. Skip Steps 1–2.

**Standalone:** Run Steps 1–2 first.

---

## Step 1 — Get the source (standalone only)

Ask Dan:

- **Meeting file path?** (e.g. `meetings/2026-05-24-growify-call.md`) — read the file and use its Summary and Key Discussion sections.
- **Or paste a transcript** along with: entity name, entity type (people or projects), and meeting date.

If given a meeting file path, read it. Derive the entity and date from the frontmatter if not passed in.

---

## Step 2 — Confirm entity location (standalone only)

From the entity name, determine the file path:
- `entities/people/<entity>.md` for clients and individuals
- `entities/projects/<entity>.md` for projects and business units

Read the entity file. If it cannot be found, stop and ask Dan for the correct path before continuing.

---

## Step 3 — Update the entity file

Read the meeting's Summary and Key Discussion sections. Identify what actually shifted:
- Did the relationship state change? (e.g. proposal accepted, project paused, scope changed)
- Did a current focus item get resolved or shift priority?
- Did a new open question emerge?
- Did a tension surface or resolve?
- Were new next actions established?

Update only the snapshot frontmatter fields that changed. Leave the rest untouched. Surgical edits — do not rewrite sections that weren't touched by this meeting.

**`## Meetings` section** — append the meeting wikilink if not already present:
```
- [[YYYY-MM-DD-entity-slug-descriptor]]
```

Do not duplicate if it is already there from Step 4 of `/meeting`.

---

## Step 4 — Append to the day's DPL

Derive the quarter from the meeting date (Q1: Jan–Mar, Q2: Apr–Jun, Q3: Jul–Sep, Q4: Oct–Dec).

Locate the daily log at `calendar/<year>/Q<N>/daily/<YYYY-MM-DD>.md`.

**If the daily log exists:**

Append to its **Done** section:
```
- [Entity] <descriptor> meeting — [[YYYY-MM-DD-entity-slug-descriptor]]
```

**If the daily log does not exist:**

Note it: "No DPL for [date] — meeting is logged in `meetings/`. Run /dpl when ready to open that day's log." Do not create the daily log — that is /dpl's job.

---

## Client portal (Notion) — DEFERRED

The `<!-- TODO(client-sync): push summary to Notion client portal when integration is built -->` comment in the meeting file marks where this sync will eventually land. Do not attempt any Notion calls. Do not remove that comment.

---

## Downstream chain — context only

This skill's job ends at entity file + DPL. The chain that follows is handled by other skills:
- `/weekly-review` reads DPL Done sections (which now include the meeting link) to compile the week
- `/month-close` reads the weekly R- files to synthesise the month

This skill does not trigger those — it just ensures the meeting lands correctly in the daily record.

---

## Step 5 — Report

**Standalone:** "Done. Entity file updated ([list which fields changed]). DPL for [date]: [appended / log not found — noted]."

**Orchestrated:** Return to the orchestrator — entity fields updated (list), DPL status (appended or not found).

---

## Rules

- Surgical edits only. Do not rewrite sections that aren't relevant to this meeting.
- Never duplicate the meeting wikilink in `## Meetings`.
- DPL append is append-only — do not edit other sections of the daily log.
- If the entity file is missing, stop and flag — do not create a new one. Dan may have the path wrong.
- Do not update entity snapshot frontmatter without explicit instruction — that is /wrap's job unless Dan asks at Step 7 of /meeting.
- Do not re-read files after writing to verify.
