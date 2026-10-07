---
description: Prospecting engine — researches real SMB prospects matching Dan's targeting criteria and writes them into the Notion Prospects database.
---

# /prospect — Prospect Batch Generator

Repurposed from `scripts/ai-prospects-dashboard.jsx` (the "ProspectAI Weekly Lead Engine"). Same workflow — targeting criteria in, scored prospects with opening lines out — but writes real pages into the Notion CRM instead of rendering cards, and researches **real companies** instead of generating fictional ones.

**The CRM lives in Notion, not the vault** (migrated 2026-08-14): Prospects database at https://app.notion.com/p/a9ca780270e3429cac997bf0b1542551, under the DoAnythingNow. home page. Use the Notion MCP tools (`notion-create-pages` against that database's data source, `notion-query-database-view` to check for existing companies) — never write prospect `.md` files into the vault.

## Arguments

Optional: `$ARGUMENTS` may override targeting (e.g. `/prospect 15 UK recruiting agencies`) or batch size. Default batch: **10 prospects**.

## Step 1 — Confirm targeting

Read `ops/context.md`. Then present current targeting defaults and let Dan adjust (AskUserQuestion or plain conversation):

- **Industries** (pick from, multi): Marketing Agency, Creative Agency, PR Agency, Accounting Firm, Legal Practice, Real Estate Agency, Recruiting/Staffing, IT Services / MSP, E-commerce Brand, Healthcare Practice, Construction & Trades, Financial Advisory, Insurance Brokerage, Architecture / Design Studio, Event Management
- **Region**: United Kingdom (default — Dan is UK-based), United States, Canada, Australia, Western Europe
- **Company size**: Micro (1–10), Small (11–50), Medium (51–200)
- **Pain points to target**: Content creation bottlenecks, Manual data entry / admin overhead, Slow proposal / document generation, Poor lead follow-up / CRM hygiene, Repetitive customer support queries, Reporting & analytics delays

If `$ARGUMENTS` already specifies targeting, skip the questions and go.

## Step 2 — Research

Use WebSearch to find **real companies** matching the criteria. Good search patterns: directory listings, "top [industry] in [city]", Clutch/agency directories, LinkedIn company results surfaced in search. For each candidate, verify it exists (has a website or LinkedIn presence) and infer size/location from what you find.

**Capture the source.** For every prospect, record the exact URL where you found / verified them — their own website homepage, or the directory listing. This goes in the `source` frontmatter field so Dan can click straight through instead of re-Googling. Always prefer the company's own website over a directory page.

**Find a contact email.** LinkedIn outreach is off the table (no Sales Navigator), so the channel is **Email** and every prospect needs a reachable email. Hunt for it: check the company's contact / about page, footer, and team page (use WebSearch or WebFetch on their site). Capture the best email you find — a named decision-maker (`firstname@`) beats a generic `hello@` / `info@`, but a generic inbox is fine as a fallback. If you genuinely can't surface one, leave `email` blank and set `next_action` to "Find contact email" rather than dropping the prospect.

**Never invent a company or an email.** Only record an email you actually saw on their site or a directory. If a search round comes up thin, narrow geography or switch industry rather than fabricating. If WebSearch is unavailable, stop and tell Dan rather than generating fiction.

Skip any company already in the Notion database (query it by Company name first).

## Step 3 — Score and write

For each verified prospect, produce:

| Field | Rule |
|---|---|
| `fit_score` | 1–10 against Dan's offer (AI workflow automation for SMBs). **Drop anything under 6.** |
| `channel` | **Email** by default (no LinkedIn Sales Navigator). Use Cold Call only if no email exists but a phone number does. |
| `source` | URL where the company was found / verified — their website homepage preferred, else the directory listing. |
| `email` | Best contact email found on their site/directory. Named decision-maker beats a generic inbox; blank only if none found. |
| `ai_opportunity` | Specific pain → what automation changes. Under 200 chars. Grounded in what the research actually showed. |
| `opening_line` | Under 200 chars, references something specific about *them*. Follow global writing rules — no AI-slop patterns. |
| `linkedin_search` | Role search string for finding the decision maker (kept for later, when Navigator is available) |

Create one Notion page per prospect via `notion-create-pages` against the Prospects data source. Set `Status: new`, `Added` and `Batch` to today, `Channel: Email`. Fill `Source` and `Email` properties, and mirror name/role/email into the page's Contact section. Page body sections: `## AI Opportunity`, `## Opening Line`, `## Contact`, `## Touch Log` (empty table), `## Notes`. Leave fields blank for anything the research didn't surface.

## Step 4 — Report

Summarise the batch: count, channel split, average fit score (the JSX header stats), and the top 3 by fit with their opening lines. Remind Dan the batch is in the **To Contact** view of the Notion Prospects database.

Append a line to today's DPL under Done: "Generated prospect batch — N prospects, avg fit X.X".

## CRM lifecycle (for reference — handled manually or by future skills)

`new → contacted → replied → call-booked → won | dead`. On `won`, promote to `entities/people/` and link back to the Notion page. Update `Last Touch` + Touch Log on every interaction.
