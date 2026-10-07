# actions/ — migrated to Notion (2026-09-02)

Live actions now live in the **DoAnythingNow. Tasks Tracker** in Notion, not here.

https://app.notion.com/p/1e64c614f8098009b9e7f06fa12afd8c

Use the **Active** view — it filters out the 146 legacy rows from the 2025-era
workflow, so what you see is only what's actually live. **Board** is the kanban;
**By client** groups the same set by who it's for.

## Why

A 55-item backlog in flat markdown couldn't be sorted, filtered, or grouped, and
nothing outside this repo could see it. Notion's Tasks Tracker was already wired
to the Clients and Projects databases with a completion rollup, so reusing it
meant the relations came for free rather than building a parallel system.

## What stayed here

`done/` and `cancelled/` are frozen as the historical record — 41 closed items
that the maintenance logs in `calendar/` reference by path. Nothing writes to
them now. Git holds the full history of the migrated files if you need to see
what one looked like before it moved.

## Field mapping

| Vault frontmatter | Notion property |
|---|---|
| `title` | Task name |
| `status: backlog` / `doing` | Status: Backlog / This Week |
| `owner` | Owner (select — `Assignee` needs real Notion users, which the clients aren't) |
| `due` (ISO dates only) | Do On |
| `source` | Vault Source |
| filename slug | Vault Slug — the stable match key; don't rename it |
| body | page content |

Non-date `due` values ("ASAP", "This week", "[implied]") became a bold line at
the top of the page body rather than an invented deadline.

## Adding actions now

`/action-items` writes straight to Notion. If you're adding one by hand, set
Vault Slug to a kebab-case slug so it stays greppable and can be matched later.
