---
type: content-index
last_updated: 2026-05-10
---

# Content Library

Output folder. Every piece of content created from the IP library, DPL sessions, or weekly reviews lands here as a file.

Files are created automatically by `/linkedin-engine`. Other formats are added manually or via future skills.

---

## Structure

| Folder | What goes here |
|--------|---------------|
| `ops/content/linkedin/` | LinkedIn post drafts and live posts |
| `ops/content/tiktok/` | TikTok scripts and captions |
| `ops/content/youtube/` | YouTube Shorts scripts |
| `ops/content/skool/` | Skool community posts and module content |
| `ops/content/concepts-with-dan/` | Episode scripts and breakdowns for the Concepts with Dan series |

## File naming

`YYYY-MM-DD-[platform]-[slug].md` — e.g. `2026-05-12-linkedin-ai-without-prep.md`

## Frontmatter schema

```yaml
---
title: [hook or title]
type: content
platform: linkedin | tiktok | youtube | skool | concepts-with-dan
status: draft | live
date: YYYY-MM-DD
week: W[N]
ip_sources: []     ← fill in manually: wikilinks to IP entries this drew from
---
```

## Workflow

1. `/linkedin-engine` saves drafts here automatically after drafting
2. When a post goes live: change `status: draft` → `status: live`
3. Fill in `ip_sources` with the IP entries the post drew from
4. Open the IP entry and update `content_made: true`, add this file to `content_pieces`
5. The Base view (`IP/_content-tracker.base`) reflects the updated state

---

← [[IP/_index]] | [[self/goals]]
