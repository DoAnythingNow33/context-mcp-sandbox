---
description: "Session close — parallel-writes all context updates: daily log, index, entity snapshots, goals. Run at the end of any working session."
---

# /wrap — Session Close

Closes the session cleanly. Reads current state, proposes updates, writes everything in one pass.

---

## Step 1 — Read current state (all in parallel)

In a single parallel tool call, read:

- Today's daily log at `calendar/[year]/[quarter]/daily/YYYY-MM-DD.md`
- `index.md`
- `self/goals.md`
- Any entity snapshots that were active this session (read first 30 lines only — frontmatter is enough to compare against what changed)

If today's daily log does not exist, create it from `calendar/[year]/[quarter]/daily/_template.md` before continuing.

---

## Step 2 — Identify what changed

Based on the session, identify:

| Signal | File to update |
|--------|---------------|
| New win, task completed, or item to move to Completed | `self/goals.md` → move to Completed with today's date |
| Entity state shifted (client or family update) | `entities/people/<name>.md` → update frontmatter fields |
| Entity state shifted (business/project milestone) | `entities/projects/<name>.md` → update frontmatter fields |
| Any entity file updated | `index.md` → update `Last Updated` for that entity |
| Session produced a new tension, open question, or next action | Relevant entity file → add to the right frontmatter list |

Ask Dan one short question: **"Anything that shifted today that I haven't captured?"**

Wait for his answer. One exchange only — don't turn this into a debrief.

---

## Step 3 — Write all updates (in parallel)

In a single parallel tool call, write every file that needs updating:

- Daily log: append a `## Session Close` note if not already captured (one line — what the session covered)
- Entity snapshots: update `last_updated`, any changed frontmatter fields
- `index.md`: update `Last Updated` for any changed entity
- `self/goals.md`: move completed items, add new threads if any emerged

Do not re-read files to verify after writing — trust the write succeeded.

After all writes complete, run `python scripts/generate_digest.py` to refresh `_digest.md`. This keeps the compressed entity state current for the next session open.

---

## Step 4 — Commit (offer, don't assume)

The system generates files faster than they get committed, so the working tree drifts from git. Close that gap at wrap.

Ask once: **"Commit this session to git? (y/n)"**

If yes, run a single command:

```
git add -A && git commit -m "Session [YYYY-MM-DD]: [3–6 word summary of what changed]"
```

Use today's date and a short summary drawn from what actually changed this session (e.g. "Fadwa snapshot + 2 actions filed"). Report the commit's short hash.

If no, skip silently — don't push back.

Never `git push` — local commit only, unless Dan explicitly asks.

---

## Step 5 — Confirm

One line: **"Wrapped. [N] files updated[, committed [hash]]."**

List the files changed. Nothing else.

---

## Rules

- Never ask more than one question in Step 2.
- Never summarise the session back to Dan — he lived it.
- Never create new files unless today's daily log is genuinely missing.
- If nothing changed, say so: "Nothing to update — context is current."
