---
description: "End-of-month review — reads all weekly R- files for the closing month, synthesizes into the month file, updates context."
---

# /month-close — Monthly Review

Closes the month cleanly. Reads the weekly record, synthesizes what the month actually was, writes it once.

---

## Step 1 — Identify the month

Use `currentDate` to determine which month is closing. If it's the last 3 days of the month or the first 3 days of the next, ask Dan to confirm which month we're closing.

Resolve:
- Month file path: `calendar/[year]/[quarter]/[month]-[year].md`
- Weekly files for this month: all `R-DD-MM-YY.md` files in `calendar/[year]/[quarter]/weekly/` where the Monday date falls within the closing month

---

## Step 2 — Load source material (in parallel)

In a single parallel tool call, read:
- The month file
- All R- files for the month (read them all simultaneously — do not read sequentially)
- `self/goals.md` (for arc context — what was active this month)

The weekly R- files are the primary source material. Each R- file was synthesised from that week's DPLs and meeting summaries (via /summary); the monthly review in turn cascades into the quarterly `review.md`.

If no R- files exist for the month, tell Dan and ask if he wants to synthesize from daily logs instead. If yes, read all daily logs for the month in parallel.

---

## Step 3 — Synthesize

From the weekly reviews, extract:

**What this month was actually about** — the honest one-paragraph summary. Not what was planned. What actually happened. What shifted, what stalled, what surprised.

**Biggest wins** — 3–5 bullets. Concrete, specific. Not vague ("worked on Skool") but real ("Module 1 live, paid community launched at $55/mo").

**What didn't move** — honest. What was on the plan and didn't happen. No apology, no spin.

**Patterns and themes** — what kept coming up across weeks? Recurring tension, recurring win pattern, shift in how work is flowing. 2–3 observations only.

**Heading into next month** — one paragraph. What's live, what's unresolved, what the first priority is.

---

## Step 4 — Write the month file

Fill in the month file sections based on the synthesis. The month file structure:

```markdown
## What This Month Was About

[One paragraph — honest summary]

## Biggest Wins

- [Specific, concrete]

## What Didn't Move

- [Honest]

## Patterns and Themes

- [Observation]

## Heading Into [Next Month]

[One paragraph]
```

Preserve the existing `## Key Dates`, `## Revenue Target`, `## Projects Active This Month`, and `## Meetings` sections — do not overwrite them.

---

## Step 5 — Update context

After writing the month file, check:

- Does `index.md` need its `last_updated` updated for any entity? (Usually no — /wrap handles this during the month.)
- Are there any active threads in `self/goals.md` that closed this month? If so, note them as candidates to move to Completed — but don't move them without Dan confirming.

Ask Dan: **"Anything from this month that should close out in goals.md?"**

Wait for one answer. Update `self/goals.md` if Dan confirms.

---

## Step 6 — Confirm

One line: **"[Month] closed. [N] weekly reviews synthesized."**

List the R- files used as source.

---

## Rules

- Read all weekly files in a single parallel tool call — never sequentially.
- Do not overwrite Key Dates, Revenue Target, Projects, or Meetings sections.
- The "What This Month Was About" paragraph should be written like you'd tell someone in a sentence — not corporate, not padded.
- Never ask more than one question in Step 5.
