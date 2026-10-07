---
description: "Meeting logger — paste a transcript and get a structured meeting file, IP entries, entity sync, and action items. Fans out to three parallel sub-agents."
---

# /meeting — Meeting Orchestrator

Turns a raw Fathom transcript into a structured meeting file, then fans out to three sub-agents in parallel: IP extraction, entity + DPL sync, and action items. One command handles everything.

---

## Step 1 — Gather context

If the meeting entity, date, and descriptor were not passed with the command, ask Dan:

- **Who was this with?** (entity name — e.g. Growify, Fadwa, Jamie)
- **Date?** (YYYY-MM-DD — defaults to today if not specified)
- **One-word descriptor?** (e.g. kickoff, scope-call, review, session-1)

Derive the filename: `YYYY-MM-DD-[entity-slug]-[descriptor].md` (lowercase, hyphens only).

Determine the entity type — client/person files live at `entities/people/<entity>.md`, project files at `entities/projects/<entity>.md`. If uncertain, ask.

---

## Step 2 — Accept transcript

Tell Dan: **"Ready. Paste the transcript."**

Wait. Do not proceed until the transcript is pasted.

---

## Step 3 — Write the base meeting file

Generate and write `meetings/YYYY-MM-DD-[entity-slug]-[descriptor].md` immediately. Do not wait for the sub-agents.

### Frontmatter

```yaml
---
title: [Entity] — [Descriptor, title-cased]
type: meeting
date: YYYY-MM-DD
attendees:
  - Daniel (DoAnythingNow)
  - [Other attendees from transcript]
status: complete
---
```

### Backlink header

```
← [[entities/people/<entity>]] | [[calendar/2026/Q2/<month>-2026]]
```

Use `entities/projects/<entity>` if it is a project entity. Derive the correct quarter and month from the meeting date.

### Title heading

`# [Entity] — [Descriptor] — DD Month YYYY`

---

### Section: Summary

3–5 lines. The meat only — what changed, what was decided, what landed. No recap of what was said. If you can remove a sentence without losing signal, remove it.

Leave this placeholder comment directly below the summary block so the Notion sync TODO is visible when the file is opened:

```
<!-- TODO(client-sync): push summary to Notion client portal when integration is built -->
```

---

### Section: Key Discussion

Organise by **topic**, not chronology. Each H3 heading = one theme or decision area. For each:
- What was the core point or question?
- What was said that mattered?
- What landed, shifted, or was decided?

Do not pad. If a topic didn't produce signal, leave it out.

---

## Step 4 — Cross-link entity and month files (parallel with Step 3)

In the same parallel tool call as the meeting file write:

1. **Update the entity file** — find its `## Meetings` section and append:
   `- [[YYYY-MM-DD-[entity-slug]-[descriptor]]]`
   If no `## Meetings` section exists, add it before any `Related:` line or at the file end.

2. **Update the month file** at `calendar/2026/Q2/<month>-2026.md` — find its `## Meetings` section and append the same wikilink.

Do not update the entity snapshot frontmatter here — that happens in /wrap or at Step 7.

---

## Step 5 — Dispatch sub-agents in parallel

Launch the three sub-skills as parallel agents. Pass each one: the full transcript, the meeting file path (`meetings/YYYY-MM-DD-[entity-slug]-[descriptor].md`), the entity name, the entity type (people/projects), and the meeting date.

### Agent 1 — `/pull-ip`
Identifies Frameworks, Concepts, Techniques, Principles, Analogies, and Patterns from the transcript. Cross-references `IP/_index.md`. Writes confirmed new entries to `IP/<slug>.md` and appends rows to `IP/_index.md`. Sets `source: [[meeting-file]]` on each entry. Returns: count of new entries written and count of existing entries flagged for update.

**When orchestrated, `/pull-ip` writes new entries directly without waiting for Dan's confirm** — because the orchestrator is already a deliberate action Dan triggered. It still reports what was written.

### Agent 2 — `/summary`
Focuses on downstream sync. Updates the entity file's `current_state` and relevant snapshot fields based on what the meeting revealed. Appends the meeting to the entity file's `## Meetings` section if not already added by Step 4. Appends to the meeting day's DPL Done section: `- [Entity] <descriptor> meeting — [[meeting-file]]`. Returns: entity fields updated, DPL status.

### Agent 3 — `/action-items`
Extracts every action item. Writes the Action Items table into the meeting file. Creates one row per item in the Notion Tasks Tracker (`Status: Backlog`). Returns: count of rows created, plus any that couldn't be related to a client.

---

## Step 6 — Consolidate and confirm

After all three agents return, give one confirmation line:

**"Done. `[filename]` filed — [N] IP entries written ([M] flagged for update), entity + DPL synced, [N] action items filed ([breakdown by folder])."**

If any agent hit a problem (missing file, ambiguous entity type, etc.), surface it here with what needs manual attention.

---

## Step 7 — Snapshot update

Ask: **"Anything from this that should update the [entity] snapshot now — or save it for /wrap?"**

If Dan says update now: make the snapshot frontmatter change immediately (current_state, current_focus, open_questions, tensions, next_actions fields as needed). Update `index.md` if the entity state changed meaningfully.

If Dan says leave it: note it and stop. /wrap handles it.

---

## Rules

- Never invent attendees — only list people who appear in the transcript.
- Action items must be attributed to a specific person, never "we" or "team".
- Summary: 3 lines of signal beats 10 lines of recap. Be brutal.
- Key Discussion: organise by theme, cut anything that didn't produce a decision or insight.
- The `<!-- TODO(client-sync) -->` comment is mandatory in every meeting file — Notion integration is not built yet.
- IP entries: proper entries, not stubs. Use existing `IP/` files as the quality bar.
- Do not update entity snapshot frontmatter during the main write — that's Step 7 or /wrap.
- Do not re-read files after writing to verify.
- If the entity file or month file cannot be found, create a stub rather than failing silently — then flag it.
- The three sub-agents run in parallel. Do not wait for one before launching the others.
