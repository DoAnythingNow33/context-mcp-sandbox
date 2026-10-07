---
description: "Cross-layer pattern detection — reads self + entities + calendar together and surfaces the connections no single file shows: self↔entity mirrors, repeated deferrals, entities going quiet, recurring tensions, arc drift."
---

# /synthesis — Cross-Layer Pattern Detection

The rest of the system captures and routes. This skill **thinks across** what's been captured. It reads the self layer, the entity states, and the recent calendar together, and surfaces the handful of connections that aren't visible from any single file.

This is the skill that makes the accumulated context pay rent. Run it standalone when you want a step back, or as the reflective pass inside `/weekly-review`.

> A finding only counts if it spans **more than one file**. If an observation comes from a single file, it's not synthesis — it's a read. Cut it.

---

## Step 1 — Gather (all in parallel)

In a single parallel call, read:

- `self/arc.md` — who Dan is becoming + the Progress Notes table
- `self/goals.md` — active threads, deferred threads, recently completed
- `self/beliefs.md` and `self/identity.md` — the belief/identity layer to mirror against
- `_digest.md` — all entity snapshot states in one file (if missing, read the active `entities/people/` + `entities/projects/` snapshots)
- The latest `R-DD-MM-YY.md` and `P-DD-MM-YY.md` in `calendar/[year]/[quarter]/weekly/`

Then pull the week's ground truth: run `python scripts/extract_carry_forwards.py --days 7` and read its output (the past week's Done / Blockers / Carry-Forward / Notes sections across daily logs). If the script isn't usable, read the last 7 daily logs directly.

Run `python scripts/validate_freshness.py` first — if snapshots are stale, say so up front; synthesis built on stale state is suspect.

---

## Step 2 — Detect (the analytical core)

Look across the loaded context for patterns along these axes. Not all will fire each week — only report the ones that genuinely do.

1. **Self ↔ entity mirrors.** Where a client's pattern, block, or breakthrough mirrors something live in Dan's own arc or beliefs. These are the highest-value findings — they're the reason the self layer and the entity layer live in the same vault. (Example pattern: a client installing a capability "through lived experience" while the arc names Dan's own gap as "experience, not capability.")
2. **Repeated deferrals / slippage.** Threads that keep moving right — appearing in Carry-Forward week after week, or sitting in goals' "Someday / Deferred" and "parked" while staying nominally active. Count how many weeks. A thing deferred 3+ weeks is a decision being avoided, not a scheduling problem — name it.
3. **Entities going quiet.** Snapshots whose `next_actions` are stalled on someone else ("waiting on X"), or with no meeting logged in a long gap. Flag the ones at risk of dying quietly.
4. **Recurring tensions.** The same tension surfacing in multiple snapshots, or the same one in the weekly `R-` files across weeks (e.g. outreach vs delivery; morning block). Recurrence = it's structural, not incidental.
5. **Arc drift.** Where the week's actual behavior (DPLs) diverges from what the arc demands (morning discipline, finishing before starting, living the frameworks). Evidence from the daily logs, measured against `arc.md`.
6. **Convergence / leverage.** Where several separate threads point at one move — the single action that unblocks the most.

---

## Step 3 — Synthesize and present

Give Dan the **3–6 connections that matter** (fewer if only a few are real — never pad to a number). For each:

- **The pattern** — one or two sentences, stated plainly.
- **The evidence** — the specific files/threads it spans (`self/arc.md` 2026-06-07 ↔ `entities/people/growify`). A finding without cross-file evidence doesn't ship.
- **So what** — one concrete move, grounded in loaded context: available time (the morning block, the buffer), current entity state, and arc direction. Generic advice is worse than none.

Lead with the sharpest mirror or the most expensive deferral. This is a briefing, not a list — order by what Dan should act on first.

---

## Step 4 — Offer to persist (targeted, not automatic)

Synthesis produces durable signal. Offer to write only what earns a home:

- A **Progress Note** row in `self/arc.md` when a mirror or arc-drift insight is worth tracking over time.
- A new **tension** or **next_action** into the relevant `entities/` snapshot when a finding belongs to one entity.
- Escalate a too-long deferral: turn it into a concrete `next_action` on its entity (or a row in the Notion Tasks Tracker) so it stops floating.
- Update `self/goals.md` active threads if the synthesis shifts what matters this week.

Ask once which to persist. Write only what Dan confirms. Update `index.md`/`last_updated` if a snapshot changed.

---

## Rules

- Cross-file or it doesn't count. One-file observations are reads, not synthesis — cut them.
- Always cite the evidence. No "you seem to be" — point at the files.
- Don't invent patterns to fill space. Two real connections beat six manufactured ones.
- Ground every "so what" in loaded context — time available, entity state, arc. No generic productivity advice.
- Self↔entity mirrors are the priority signal. When one is real, lead with it.
- Apply the global anti-slop writing rules — no false "not just X but Y" framing, no rhetorical-question pivots, no forced triplets, no inspirational zoom-out.
- This is read-and-reflect by default. Write nothing until Step 4, and only what Dan confirms.
- Don't re-read files after writing to verify.
