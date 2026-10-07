---
description: "Action item extractor — pulls every action item from a meeting transcript, writes the table into the meeting file, and creates one row per item in the Notion Tasks Tracker."
---

# /action-items — Action Item Extractor

Extracts action items from a meeting transcript, writes the Action Items table into the meeting file, and creates one row per item in the **Notion Tasks Tracker**. Runs as Agent 3 inside `/meeting`, or standalone on any transcript or meeting file.

> **Actions moved to Notion on 2026-09-02.** `actions/backlog/` and `actions/doing/` no longer exist as a kanban — `actions/done/` and `actions/cancelled/` are a frozen archive. Never create new files there. See `actions/README.md`.

---

## Mode detection

**Orchestrated (called by `/meeting`):** The transcript, meeting file path, entity name, and meeting date are passed in. The meeting file already exists. Go straight to Step 3. Write the table into the meeting file and file all items without waiting for a confirm gate.

**Standalone:** Run Steps 1–2 first.

---

## Step 1 — Get the source (standalone only)

Ask Dan:

- **Meeting file path?** (e.g. `meetings/2026-05-24-growify-call.md`) — read the file to get the transcript or Key Discussion content.
- **Or paste a transcript** and provide: the meeting file path (so action items can be written back into it), the entity name, and the meeting date.

If a meeting file path is given and no transcript is pasted, use the Key Discussion and any existing Content sections from the file as the source.

---

## Step 2 — Confirm meeting file path (standalone only)

Verify the meeting file exists before proceeding. If it cannot be found, ask Dan to confirm the path. Do not create a new meeting file here — that is `/meeting`'s job.

---

## Step 3 — Extract action items

Scan the transcript for every commitment, task, or next step. Apply this bar: if someone said they would do something — or if the meeting clearly implies it needs doing — it is an action item.

**Every item must have:**
- **Owner** — a specific person. "We" is not an owner. If a task was discussed without a clear owner, assign it to Daniel if he's the obvious responsible party; otherwise flag it as `[owner unclear]` and list it anyway.
- **Action** — the concrete thing to do. One sentence. Specific enough that the owner knows exactly what's expected.
- **By** — a date, day, or "ASAP" if no deadline was stated. If the meeting implies urgency, use "ASAP". If it is clearly for next week, use the day name.

---

## Step 4 — Write the Action Items table into the meeting file

Append (or replace if a stub exists) the `## Action Items` section in the meeting file:

```markdown
## Action Items

| Owner | Action | By |
|-------|--------|----|
| Daniel | [specific action] | [date or ASAP] |
| [Other] | [specific action] | [date or ASAP] |
```

Use the owner's first name. Daniel = Dan's full name in the table for clarity. Other attendees: use first name as it appears in the transcript.

---

## Step 5 — Create rows in the Notion Tasks Tracker

Create one page per action item in the **DoAnythingNow. Tasks Tracker**
(data source `1e64c614-f809-80b6-944a-000b9e6dfad4`), using `notion-create-pages`.
Create them all in a single call.

| Property | Value |
|---|---|
| `Task name` | the action, one imperative sentence |
| `Status` | `Backlog` for anything newly captured. Only `This Week`/`Today` if it is genuinely already underway. |
| `Owner` | select — `Daniel`, `Rishab`, `Disha`, `Victoria`, `Fadwa`, `Jamie Cameron`, `Sam`, `Daniel + Rishab`. Add a new option rather than forcing a wrong fit. |
| `Vault Slug` | short kebab-case slug, max 5 words, no dates — e.g. `send-invoice-growify`. This is the stable match key; keep it unique. |
| `Vault Source` | the meeting wikilink, e.g. `[[2026-05-24-growify-call]]` |
| `Clients ` | JSON array holding the client page URL, when the action clearly belongs to one (note the trailing space in the property name) |
| `date:Do On:start` | **ISO dates only** (`YYYY-MM-DD`). Never pass "ASAP" or a day name — Notion rejects it. |
| `Priority` | `High` only when the meeting made urgency explicit. Leave unset otherwise. |

**Non-date deadlines.** If the meeting said "ASAP", "this week", or the date is
only implied, do not invent one. Leave `Do On` empty and open the page body with
`**Urgency noted in the meeting:** ASAP`.

**Page body:** one or two sentences of context only if it's needed to actually do
the task, then a provenance line naming the meeting it came from. Don't restate
the title.

**Client page URLs** — fetch the Clients data source
(`2224c614-f809-80bd-b4e7-000b8ee69a46`) to resolve these. If a client has no row
yet, create the action unrelated and flag it in the report rather than guessing.

---

## Step 6 — Report

**Standalone:** "Done. [N] action items extracted, [N] created in Notion. Table written to `meetings/[filename]`." Include the Notion URL of each created row, and name anything left without a client relation.

**Orchestrated:** Return to the orchestrator — count of rows created, plus any that could not be related to a client.

---

---

## Step 7 — Sync to Google Calendar

After creating the Notion rows, run `/gcal` to push Dan's new items to Google Calendar.

**Standalone mode only** — if any of the newly filed items have owner "Daniel" or "Dan", prompt: "Run `/gcal` to add these to Google Calendar? (yes/skip)" — wait for response. If yes, invoke `/gcal`.

**Orchestrated mode** — do not auto-run `/gcal`. The orchestrator (`/meeting`) will decide whether to trigger it. Return the count of Dan-owned items to the orchestrator so it can decide.

---

## Rules

- "We" is not an owner. Attribute every item to a person.
- If an action is clearly implied but not explicitly stated, include it and flag it with `[implied]` in the By field so Dan can review.
- One Notion row per action item — do not bundle multiple actions into one row.
- Query the Tasks Tracker for existing `Vault Slug` values before creating, and skip anything already there. `/maintain` twice filed the same logo task under two slugs a day apart — that's the failure this prevents.
- Do not create the meeting file itself — only append/write the Action Items section into an existing file.
- Do not re-read files after writing to verify.
- Never write new files into `actions/` — it is a frozen archive.
