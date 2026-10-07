---
description: "Google Tasks sync — dumps all Dan's backlog actions into Google Tasks. Run at end of /weekly-review or after /action-items."
---

# /gcal — Google Tasks Sync

Reads all backlog action items owned by Dan and creates Google Tasks entries, so he can work through them from any device.

---

## Step 1 — Read backlog

Query the Notion Tasks Tracker (data source `1e64c614-f809-80b6-944a-000b9e6dfad4`) for rows where `Status` is `Backlog`, `This Week`, or `Today` and `Owner` is Daniel. If none come back, say "No open items found. Nothing to sync." and stop.

---

## Step 2 — Parse and filter

For each file read, extract the frontmatter fields: `title`, `owner`, `due`, `status`, `source`.

Keep only items where `owner` is "Daniel", "Dan", or any clear first-name variant of Dan (case-insensitive). Discard items where the owner is someone else.

---

## Step 3 — Check for existing tasks

Call `mcp__gtasks__list` to get all current Google Tasks. Build a set of existing task titles so you can skip duplicates (exact title match, case-insensitive).

---

## Step 4 — Find Monday of current week

Calculate the date of Monday of the current ISO week (the Monday on or before today). Format as `YYYY-MM-DDT00:00:00.000Z`.

---

## Step 5 — Create tasks

**Important:** always pass `title` in every `mcp__gtasks__update` call — omitting it will blank the title.

For each qualifying action item not already in Google Tasks, call `mcp__gtasks__create`:

- **title**: the `title` field from the action file
- **notes**: `Source: [source] | Due: [due]` (omit fields that are empty)
- **due**: Monday of current week, formatted as `YYYY-MM-DDT00:00:00.000Z`

Run creates sequentially.

---

## Step 6 — Confirm

After all tasks are created, print:

> ✓ [N] tasks added to Google Tasks on Monday [YYYY-MM-DD] ([X] skipped as duplicates). Go to Google Calendar and drag them to the right day/time.
