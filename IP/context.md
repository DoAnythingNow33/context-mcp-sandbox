# IP/ — Knowledge Library

## What this workspace is for

Atomic knowledge base. Every concept, technique, framework, principle, or analogy extracted from sessions, meetings, or thinking. This is the source material for coaching, consulting, and content — the library that builds the brand. The `content/` subfolder is the output layer where IP becomes posts and scripts.

## Structure

```
IP/
├── _index.md              — Full table: Name | Type | Tags | First Seen | File
├── _template.md           — Schema for new entries
├── _content-tracker.base  — Obsidian Base view: what IP has been converted to content
├── [slug].md              — One file per concept, technique, or framework
└── content/               — Output layer: where IP becomes published content
    ├── context.md         — Content workspace guide
    ├── _index.md          — Content library overview
    ├── linkedin-audience.md
    ├── linkedin/          — LinkedIn drafts (YYYY-MM-DD-[slug].md)
    │   ├── Posted/        — Published pieces
    │   └── Deferred/      — Paused or deprioritised drafts
    └── x/                 — X/Twitter threads (YYYY-MM-DD-[slug].md)
        ├── Posted/
        └── Deferred/
```

## Entry schema (from _template.md)

Frontmatter: `name`, `type`, `tags`, `source`, `first_seen`, `last_updated`, `content_made`, `content_formats`, `content_pieces`

The `content_made` flag tracks whether an IP entry has been converted to a post or script. Set to `true` when it has; add the content link under `content_pieces`.

Sections: What It Is | Why It Matters | How to Use It (coach / consultant / content creator) | Content Angles | Seen In

## Process

1. New entries are auto-created by `/meeting` when a concept surfaces in a session
2. Manual entries: copy `_template.md`, fill it, add a row to `_index.md`
3. When an IP entry becomes a post or script: set `content_made: true`, add the link under `content_pieces`
4. Use `_content-tracker.base` to see what's been deployed and what hasn't

## When to load this workspace

- IP development sessions: read `_index.md` + the specific entry
- Before `/written-content`: scan `_index.md` for entries with `content_made: false`
- After a client session: check if any new concept warrants a new entry

## Skills that apply here

| Skill | When |
|---|---|
| `/meeting` | Writes to IP automatically when a concept surfaces |
| `/pull-ip` | Extracts frameworks, concepts, techniques, principles, analogies, and patterns from a transcript or meeting file — writes them to IP library |
| `/written-content` | Pulls unused IP + weekly review + audience profile to generate 8 post ideas; Dan picks; engine drafts 4 LinkedIn posts and 7 X tweets |
