# /weekly-review

Sunday weekly review and planning session for Context 2.0.

## What this command does

Runs in two phases. Phase 1 is automated. Phase 2 requires Dan's input and green light before anything is written or sent.

---

## Phase 1 — Review (automated)

0. **Run naming validation**: `python scripts/validate_naming.py`. If violations are found, show the list and ask Dan to confirm before proceeding. Don't block — just surface.

   **Optional pre-processing**: If you want to reduce token load, run `python scripts/extract_carry_forwards.py --days 7 --output calendar/[year]/[quarter]/weekly/_week-data.md` before this session. If `_week-data.md` exists in the weekly folder, read it in Step 2 instead of reading all 7 daily logs individually.

0.5. **Check for pre-generated gap questions** — look for `_review-questions.md` in the current week's `calendar/[year]/[quarter]/weekly/` folder. This file is written automatically every Sunday by the `com.dananything.weekly-questions` LaunchAgent (`scripts/generate_review_questions.py`), which inspects the week and asks the questions the DPLs can't answer.

   **If it exists, run it FIRST, before anything else:**
   - Read it and present the questions to Dan conversationally — work through them block by block (one missing day or plan-item group at a time, not a wall of 14 questions). Pre-fill anything you can already confirm from snapshots, meeting files, or `actions/done/` so he only answers true gaps.
   - Capture his answers as you go. These become primary source material for Step 3 — treat them with the same weight as a DPL.
   - Once answered, **archive the file**: rename it to `_review-questions-answered-DD-MM-YY.md` (the week's Monday date) so the next Sunday run starts clean and the answers stay on record. Do not leave the un-archived file in place.

   If it does **not** exist (e.g. the LaunchAgent isn't active yet, or it's not Monday), fall through to the manual gap-filling in Step 2.

1. **Load orientation files**: `index.md`, `self/goals.md`, and the previous week's plan file (`P-DD-MM-YY.md`) from `calendar/[year]/[quarter]/weekly/`.

2. **Read source data** — if `_week-data.md` exists in the weekly folder (from pre-processing), read that single file. Otherwise, read all daily logs from `calendar/[year]/[quarter]/daily/` for the past 7 days **in a single parallel tool call**. Note any days with no log.

   **If no DPL logs exist for the week (or fewer than 3 days are logged) AND `_review-questions.md` was not present in Step 0.5:**
   - Show Dan the previous week's plan (`P-DD-MM-YY.md`) line by line as the source of truth for what was intended
   - Pull evidence of what actually moved from the Notion Tasks Tracker (data source `1e64c614-f809-80b6-944a-000b9e6dfad4`): rows moved to `Done` in the past 7 days are what completed; rows still in `Backlog`/`This Week`/`Today` are what's open. Notion is the source of truth for actions; `actions/done/` in the vault is a frozen pre-2026-09-02 archive.
   - Present both (plan + completed actions) to Dan clearly
   - Ask targeted questions to fill the gaps — one block per day where there's no data, or per major planned item. For example: "The plan had 100x100 outreach Wed–Fri — did any happen? What was the actual count?" Don't ask generic "how did the week go" — ask specifically about each planned item that can't be confirmed from snapshots, meeting files, or `actions/done/`.
   - Wait for Dan's answers before synthesising or writing the review file.

   (This manual path is the fallback for when the Sunday LaunchAgent didn't run. When `_review-questions.md` exists, Step 0.5 has already collected these answers.)

3. **Synthesise the week**: wins, what moved, what stalled, carry-forwards, open questions. Cross-reference against last week's plan — what was on it, what got done, what didn't.

4. **Write the weekly review file** as `R-DD-MM-YY.md` in `calendar/[year]/[quarter]/weekly/`. Use the Monday start date of the week just ended (dd-mm-yy, no slashes). Format matches existing weekly logs.

5. **Update context** — read entity snapshots for synthesis by reading only the first 30 lines (frontmatter + current_state are sufficient; do a full read only if you need to write an update). Each person or project is its own file — read the relevant files from `entities/people/` (clients and family) and `entities/projects/` (business). Run these reads in parallel:
   - Update `index.md` if any entity state changed
   - Update any entity files that shifted (`entities/people/<name>.md` or `entities/projects/<name>.md`)
   - Update `self/goals.md` if active threads changed
   - Write all updates in parallel — do not write sequentially.

   Note: meeting summaries captured in the daily logs (via /summary) are part of the source material this review synthesises. The weekly review in turn feeds the monthly synthesis (via /month-close), which feeds the quarterly review.

6. **Extract all open tasks and carry-forwards** — consolidate into a single prioritised list.

7. **Synthesis pass** — run the `/synthesis` analysis (Steps 2–3 of that skill) over the now-loaded self + entity + week data. Surface the 3–6 cross-layer patterns that should shape the coming week: self↔entity mirrors, deferrals slipping (count the weeks), entities going quiet, recurring tensions, arc drift. Carry these into Phase 2 — the plan should answer them, not ignore them. Persist any durable findings per `/synthesis` Step 4 with Dan's nod.

---

## Phase 2 — Plan (collaborative, requires green light)

Present the following to Dan and **wait for his input before proceeding**:

- The consolidated task list from Phase 1
- A draft priority order for the coming week — what to focus on Mon–Fri across deep work blocks, based on: entity states, arc direction, available time (5 hrs/day Mon–Fri), and anything time-sensitive
- Any tensions or sequencing conflicts that need a decision

**Ask Dan**: Does this feel right? What would you move, drop, or add? What needs to happen by a specific day?

Once Dan confirms the plan:

8. **Write the weekly plan file** as `P-DD-MM-YY.md` in `calendar/[year]/[quarter]/weekly/`. Use the Monday start date of the coming week.

   Structure:
   - North star for the week (one sentence)
   - Day-by-day breakdown (Mon–Fri) with named tasks per deep work block
   - Any fixed commitments or deadlines
   - What's being deliberately parked

9. **File the week's actions into Notion** — present the full list of concrete next steps the plan implies, with suggested due dates. Wait for Dan's final confirmation, then create one row per action in the Tasks Tracker (data source `1e64c614-f809-80b6-944a-000b9e6dfad4`): `Task name`, `Owner`, `Status: Backlog`, `Vault Slug` (fresh kebab slug), `Vault Source` → this week's `P-` file, `Clients ` where it belongs to one, and `date:Do On:start` only for real ISO dates. Check existing `Vault Slug` values first so you don't double-file.

   Only create action files after explicit green light from Dan.

10. **Populate the weekly planner** — once the P- file is written and the backlog actions are confirmed, write `visual/weekly-schedule.json` directly. You already have full context: the P- plan's day-by-day breakdown, the active threads, and the new action files. Use that to assign each action (backlog + doing) to a specific day (Monday–Friday). Rules:

    - Doing items go first — assign them early in the week
    - Client-facing items (owner is not Dan) go before internal tasks
    - No more than 4 items per day; leave Friday lighter as a catch-up buffer
    - Items tied to a specific day in the P- plan go on that day
    - Items with a due date go on or before that date

    Write the file in this exact shape (ISO week in `week`, exact `.md` filenames as values):

    ```json
    {
      "week": "YYYY-WNN",
      "monday": ["filename.md"],
      "tuesday": [],
      "wednesday": [],
      "thursday": [],
      "friday": []
    }
    ```

    Compute the ISO week string: year + `-W` + zero-padded week number of the *coming* Monday (the week being planned). After writing, say: "Weekly planner populated — open the Actions tab in the dashboard to review and adjust."

---

## File naming reference

| File | Name format | Example |
|------|-------------|---------|
| Daily log | `YYYY-MM-DD.md` | `2026-05-03.md` |
| Weekly review | `R-DD-MM-YY.md` | `R-20-04-26.md` |
| Weekly plan | `P-DD-MM-YY.md` | `P-27-04-26.md` |
| Monthly | `[month]-[year].md` | `may-2026.md` |
| Quarterly review | `calendar/[year]/[quarter]/review.md` | `calendar/2026/Q2/review.md` |

---

## Quarter folder reference

| Quarter | Path |
|---------|------|
| Q2 2026 (Apr–Jun) | `calendar/2026/Q2/` |
| Q3 2026 (Jul–Sep) | `calendar/2026/Q3/` |
| Q4 2026 (Oct–Dec) | `calendar/2026/Q4/` |
| Q1 2027 (Jan–Mar) | `calendar/2027/Q1/` |
