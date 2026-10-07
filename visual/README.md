# visual/ — Micro-App Layer

Everything Dan has built as a browser-based interface on top of the Context 2.0 vault, plus the client pitch decks built the same way. This folder is code and AI-built artifacts, not vault content — nothing here follows the entity/calendar/IP conventions in the root `CLAUDE.md`.

## Structure

```
visual/
├── app/       — the "Command Centre" dashboard (index.html) — kanban over actions/, calendar view
├── pitches/   — client/project pitch decks, each a standalone static site
│   ├── jamie-pitch/       — pitch deck for Jamie Cameron (has its own .vercel deploy config)
│   └── sleevenote-pitch/  — pitch deck for the Sleevenote project
└── misc/      — one-off pages and orphaned data files, not wired into anything active
```

## app/

`app/index.html` is a static dashboard reading `app/calendar-events.json`. Per project history it originally had a Python backend (`server.py`, port 8765) providing a live actions-kanban and a CRM tab reading `ops/sales/prospects/` — that backend is gone from the repo (only stale `.pyc` bytecode remained, now removed) and the CRM tab's data source no longer exists as of 2026-08-14 (prospects CRM migrated to Notion — see `ops/sales/context.md`). Treat `app/` as a static shell until/unless the backend is rebuilt. Full history: memory `project-visual-layer`.

## pitches/

Each pitch deck is a self-contained static site (own assets, own `index.html`). `jamie-pitch/` carries its own `.vercel` and `.gitignore`, meaning it was deployed independently — check there before assuming it's just a local file.

## misc/

`dan-logo-3d.html` (+ a `copy` variant) and `portfolio.html` are standalone personal pages, not connected to `app/`. `baby-calendar-events.json` and `weekly-schedule.json` are data files not referenced by `app/index.html` — orphaned, kept for now rather than deleted since their origin wasn't confirmed.

## Why this structure

Reorganized 2026-08-14 — previously `app/`, the pitch decks, and personal one-offs were flat in `visual/` with no separation, making it unclear which files were live app code vs. archived client work vs. unrelated personal pages.
