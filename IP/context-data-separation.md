---
name: Context-Data Separation
type: principle
tags: [AI, consulting, systems, methodology, context, data, maintenance, architecture]
source: [[2026-06-13-growify-session-1]]
first_seen: 2026-06-13
last_updated: 2026-06-13
content_made: false
content_formats: []
content_pieces: []
---

# Context-Data Separation

## What It Is

Context and data are fundamentally different kinds of information and must live in separate systems:

- **Context**: how things are done, who does what, brand voice, workflows, team structure, client knowledge. Changes slowly. Updated through conversations and decisions. Best stored in lightweight text-based systems the AI can read directly.
- **Data**: numbers, metrics, dashboards, analytics. Changes constantly. Updated by events and transactions. Best stored in queryable databases with defined schemas.

Mixing them into one system creates maintenance conflicts: data needs event-triggered updates, context needs deliberate human input. When they share a home, the data goes stale and the context gets buried under noise.

## Why It Matters

The most common ops build failure mode is the "everything in Notion" trap — trying to store workflows, dashboards, meeting notes, and client metrics in the same tool. The result is a system that's too slow for data and too noisy for context. AI agents can't navigate it cleanly because the signal-to-noise ratio collapses.

Separation solves this by matching information types to appropriate containers. Context lives somewhere lightweight and AI-readable. Data lives somewhere queryable and event-driven. Neither bleeds into the other.

## How to Use It

**As a coach:** If a client's knowledge management system feels overwhelming, ask: is this a place for how we work, or a place for what's happening? If the answer is both, the system is trying to be two things and failing at both.

**As a consultant:** This is the diagnostic question in every ops audit. For each tool: is it storing context or data? If it's doing both, that's the problem. The fix is decomposition, not better organisation within the same tool.

**As a content creator:** You don't need a better Notion. You need Notion to stop trying to be your analytics platform.

## Content Angles

- The reason your knowledge base feels chaotic isn't the information — it's that you've mixed two different types of information with different half-lives.
- Context is a slow burn. Data is a live feed. They need different homes.
- Notion was never meant to be your analytics dashboard. That's why your analytics dashboard feels like noise when you open Notion.

## Seen In

- [[2026-06-13-growify-session-1]] — Named explicitly in session: context folder stores how things are done (workflows, brand knowledge, team structure); PostHog stores analytics (Shopify data, ad spend, dashboards). The conversation identified that mixing these two had been a core source of Growify's ops bloat and maintenance friction.
