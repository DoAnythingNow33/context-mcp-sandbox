# ops/content/ — Output & Distribution

## What this workspace is for

The output layer. Where IP becomes posts and threads. Everything published or queued for publication lives here, organised by platform. Files link back to the IP entries they drew on. This folder lives under `IP/` because content is the deployed form of IP — not a separate system.

## Structure

```
ops/content/
├── _index.md              — Content library overview
├── brand.md               — Visual identity: colours, typography, logo
├── linkedin-audience.md   — Audience profile (loaded before any content creation)
├── linkedin/              — LinkedIn posts (YYYY-MM-DD-[slug].md)
│   ├── Posted/            — Published pieces (moved here after going live)
│   └── Deferred/          — Paused or deprioritised drafts
└── x/                     — X/Twitter threads (YYYY-MM-DD-[slug].md)
    ├── Posted/
    └── Deferred/
```

## File schema

```yaml
---
title: [Post title]
type: [post | thread | carousel]
platform: [linkedin | x]
status: [draft | live]
date: YYYY-MM-DD
week: [R-DD-MM-YY]
ip_sources: ["[[IP/[slug]]]"]
---
```

## Workflow

1. `/written-content` pulls unused IP (`content_made: false`), the weekly review, and `linkedin-audience.md` to generate 8 post ideas
2. Dan picks; engine drafts 4 LinkedIn posts and 7 X tweets in his voice — saved here
3. After publishing: move the file to `Posted/` and update `status: live`
4. In the source IP entry: set `content_made: true`, add the content link under `content_pieces`
5. For paused drafts: move to `Deferred/` rather than deleting

## Always load with this workspace

`self/writing-dna.md` — voice and structural patterns. Load it before any content creation, every time.

`ops/content/brand.md` — colours, typography, logo, and visual identity. Load for any design, web, or visual content work.

## Skills that apply here

| Skill | When |
|---|---|
| `/written-content` | Weekly — generates 8 ideas, drafts 4 LinkedIn posts + 7 X tweets from unused IP |

Content tracker: `IP/_content-tracker.base` shows what IP has been deployed vs. what hasn't.
