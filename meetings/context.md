# meetings/ — Meeting Records

## What this workspace is for

Single source of truth for all meetings. One file per meeting, named by date and slug. Meeting files do not duplicate entity state — they link to it.

## Structure

```
meetings/
├── YYYY-MM-DD-[slug].md    — Active meeting files
└── archived/               — Pre-vault or low-reference meetings; same format
```

## File naming

`YYYY-MM-DD-[client-or-topic-slug].md`

Examples: `2026-06-13-growify-session-1.md`, `2026-05-15-fadwa-session-5.md`

## Frontmatter schema

```yaml
---
title: Client — Session or Topic Description
type: meeting
date: YYYY-MM-DD
attendees:
  - Name (Role, Org)
duration: ~N mins
entity: entity-slug
---
```

## Linking convention

Every meeting file opens with a backlink header:
```
← [[entities/people/growify]] | [[calendar/2026/Q2/june-2026]]
```

Each entity file referenced has a `## Meetings` section listing this file. Each calendar month file has the same `## Meetings` section. The meeting file is the source; entity + calendar files are the index.

## Skills that apply here

| Skill | When |
|---|---|
| `/meeting` | After any meeting — paste transcript, orchestrates the full ingest |
| `/pull-ip` | Extracts IP from meeting content → `IP/` database |
| `/summary` | Updates the entity file and DPL from meeting content |
| `/action-items` | Extracts next steps → Notion Tasks Tracker |
