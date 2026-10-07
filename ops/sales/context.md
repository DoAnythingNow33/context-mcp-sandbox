# ops/sales/ — Outbound Pipeline

## What this workspace is for

The prospecting CRM lives in **Notion**, not the vault — a relational pipeline (status, fit score, days-since-touch) is a better fit for a real database than markdown + frontmatter. Every company Dan is considering reaching out to is a page in the **Prospects** database: https://app.notion.com/p/a9ca780270e3429cac997bf0b1542551 (under the DoAnythingNow. home page). The pipeline moves from research → contact → reply → call → won/dead. Views: **Pipeline** (board, grouped by Status) and **To Contact** (status = new, sorted by fit score).

**Migrated 2026-08-14.** The old vault-based version (51 prospects, one `.md` per company + `prospects.base`) is archived at `ops/sales/archive/prospects-pre-notion-2026-08-14/` — kept for history, not read by any skill anymore.

## Structure

```
ops/sales/
├── ai-workflows-outreach-playbook.md  — Messaging strategy and opening-line patterns
└── archive/                  — Retired vault-based CRM (pre-2026-08-14), reference only
```

## Status pipeline

`new → contacted → replied → call-booked → won | dead`

- **won** → graduate to `entities/people/[slug].md` + link back to prospect file. Prospect file stays as origin record.
- **dead** → leave in place; useful for anti-pattern recognition.

## Scoring

`fit_score` is 1–10. Anything under 6 doesn't get a file. Scores are set by `/prospect` at research time based on size, location, industry, and evidence of pain.

## Rules

- Prospects are real companies verified by research. Never invented.
- Every contact attempt gets a row in the page's `## Touch Log`.
- `/prospect` generates a researched batch and writes pages directly into the Notion database; Dan works the "To Contact" view in Notion to send and update status.

## Skills that apply here

| Skill | When |
|---|---|
| `/prospect` | Weekly outbound prep — generates a researched batch of new prospects |
