# calendar/ — Time Layer

## What this workspace is for

The time structure. Daily capture, weekly rhythm, monthly synthesis, quarterly planning. This is where work gets dated, reviewed, and carried forward.

## Structure

```
calendar/
└── [year]/[quarter]/
    ├── daily/             — YYYY-MM-DD.md (DPL logs)
    ├── weekly/            — R-DD-MM-YY.md (review) + P-DD-MM-YY.md (plan)
    │                        _week-data.md (optional pre-processed extract)
    ├── [month]-[year].md  — Monthly review
    └── review.md          — Quarterly review
```

## Naming conventions

| File | Format | Example |
|---|---|---|
| Daily log | `YYYY-MM-DD.md` | `2026-05-20.md` |
| Weekly review | `R-DD-MM-YY.md` | `R-18-05-26.md` |
| Weekly plan | `P-DD-MM-YY.md` | `P-25-05-26.md` |
| Monthly | `[month]-[year].md` | `may-2026.md` |

## Process

- **Daily:** `/dpl` opens capture mode (also used as a coaching DPL for client sessions) — voice updates from Telegram queue are auto-imported and classified into the correct sections; meeting summaries from `/summary` land here too
- **Session close:** `/wrap` writes to today's daily log, updates index, entity snapshots, and goals in a single parallel pass — then regenerates `_digest.md`
- **Weekly:** Run `python scripts/extract_carry_forwards.py --days 7` first (cuts tokens ~80%), then `/weekly-review` to synthesise and write R- + P- files
- **Monthly:** `/month-close` reads all R- files for the month and writes the monthly review
- **New quarter:** `python scripts/scaffold_quarter.py [year] [Q]` creates the full folder structure

## Skills that apply here

| Skill | When |
|---|---|
| `/dpl` | Start of workday or any time you have updates |
| `/wrap` | End of every session |
| `/weekly-review` | Sunday |
| `/month-close` | Last day of month |
| `/braindump` | Categorise a brain dump into sprint structure |
