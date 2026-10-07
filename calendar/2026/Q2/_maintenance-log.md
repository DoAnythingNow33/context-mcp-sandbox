---
type: maintenance-log
last_updated: 2026-06-22
---

# Maintenance Log — Q2 2026

Append-only record of every `/maintain` run. This is Dan's review surface — scan the "Flagged for Dan" sections.

## 2026-06-22 — /maintain
**Health: 38/100** (was 36 — first real sweep; decay items left for Dan dominate the score)

### Auto-fixed
- Index drift: `index.md` Growify row 2026-05-10 → 2026-06-13 (matched snapshot)
- Index drift: `index.md` Sam / Explorers Club row 2026-05-12 → 2026-05-24 (matched snapshot)
- Regenerated `_digest.md` (8 entities) after fixes
- Filed 11 unfiled snapshot next_actions as `actions/backlog/` items: Fadwa (content direction, £80/mo billing), Family (childcare conversation, date night, August household prep), Jamie (chase Social Trait, next engagement), Santiago/Bonita (Instagram series, formalise equity, brand list + decks), Shereen (confirm scope)
- Misfiled actions: none found (all status/folder aligned)

### Acted (judgment)
- Quiet entity **Explorers Club** → filed `explorers-club-chase-sam` (no open action existed; Sam 29d quiet, waiting on him to book). This also resolves the past-dated "Wed 27 May final meeting" next_action.
- Quiet entities **Fadwa / Family / Santiago / Shereen** → already covered by the actions filed above; no check-in created.
- Skipped 2 unfiled next_actions as duplicates of existing actions: Fadwa "Circa Arts / Joseph follow-up" (covered by 2 existing Circa actions), Growify "PostHog follow-up" (covered by 2 existing PostHog actions)
- Rotting actions (7, 17–27d) → all judged still relevant (active Growify delivery + Fadwa follow-through); left in place, annotated with a `/maintain` note. Not dropped — they're real, just stalled.
- Parked threads → all 3 are "waiting" states, not dead; left in `self/goals.md` untouched (Shereen + Sam now have backing actions; Claude Architect Certificate flagged below)
- Unused IP (13 entries >30d) → queued to `IP/content/_idea-queue.md` for `/written-content`

### Flagged for Dan (needs your call)
- **`entities/projects/snapshot.md` (DoAnythingNow) is 43 days stale.** Its 6 "next_actions" are old daily-plan fragments — several already done (Modules 2/3/4 posted, Growify invoice sent). I did NOT file them as actions. **Refresh this snapshot** (run `/wrap` or edit directly); it's the single biggest source of false signal in the vault.
- **Claude Architect Certificate** thread is parked "until Growify sessions settle" — those sessions ended 21 Jun. Decision: give it a named block now, or move to Someday/Deferred?
- **Sam / Explorers Club** 29d quiet — chase action filed. If no response, do you call the engagement done?
- **DPL gaps:** 9 of last 14 days unlogged (Jun 9,10,11,14,17,18,19,20,21). Not backfilled — log retroactively if the data exists. This is the biggest lever on the health score.
- **Commit→done last 7d: 1 done / 0 created before this run** — backlog is growing faster than it clears (now 23 items). Worth a focused clear-down.

## 2026-06-22 — /maintain (interview applied)
**Health: 57/100** (was 38 — suppressions + thread cleanup)

### Applied from interview
- Q1 DoAnythingNow stale snapshot → "you refresh it for me": draft signed off and written to `entities/projects/snapshot.md` (last_updated 2026-06-22); index row updated; filed `growify-phase-2-proposal` from the refreshed next_actions. Score 57 → 63; freshness check now clean.
- Q2 Sam alive → real next move is build his Notion setup this week then send to finish together. Replaced `explorers-club-chase-sam` with `explorers-club-sam-notion-setup`; reworded the Sam thread in `self/goals.md`.
- Q3 Claude Architect Certificate not feasible → dropped from `self/goals.md`, replaced with "Skilljar certificates — 2 of 5, get 3 more"; filed `get-3-more-skilljar-certificates`.
- Q4 DPL gaps → "gone is gone": added 9 dates to `scripts/.health-suppress.json` (excluded from the gap count).
- Q5 backlog ratio → "leave it": muted `acct.ratio` until 2026-07-06 in `scripts/.health-suppress.json`.

### Auto-fixed
- Wired suppression support into `scripts/system_health.py` (`.health-suppress.json`: `dpl_gap_dates` + `suppress_until`) so resolved items stop re-nagging on the nightly run.

### Acted (judgment)
- Re-ran `system_health.py`: 38 → 57 (DPL penalty −9 and 2 parked-thread penalties cleared).

### Queued for interview
- None — interview fully answered and archived.
