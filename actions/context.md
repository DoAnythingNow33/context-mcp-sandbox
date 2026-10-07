# actions/ — Kanban

## What this workspace is for

Action database. Every concrete next step lives here as its own file — one file per action item, filed into one of three columns by status. This is where meeting outputs land and where weekly planning happens. A custom HTML viewer reads these folders directly and renders the board.

## Structure

```
actions/
├── _template.md     — Schema for new action items
├── context.md       — This file
├── backlog/         — Captured, not started
├── doing/           — Actively being worked
└── done/            — Completed (kept for reference, not deleted)
```

## Entry schema (from _template.md)

Frontmatter: `title`, `owner`, `due`, `status` (backlog/doing/done), `source` (wikilink to the meeting or session it came from)

Body: freeform notes on the action — context, dependencies, definition of done.

## How it works

- New items are created by the `/action-items` skill after a meeting — one file per item, dropped into `backlog/`
- To start work: move the file to `doing/` and update the `status` field
- To complete: move the file to `done/` and update `status: done`
- The HTML viewer (planned) reads these folders and renders them as a drag-and-drop board

## When to load this workspace

- At the start of any planning session — scan `backlog/` and `doing/`
- After a meeting — check what `/action-items` dropped in
- During weekly review — pull from `backlog/` into `doing/` for the week ahead
