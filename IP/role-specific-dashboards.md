---
name: Role-Specific Dashboards on a Shared Data Layer
type: framework
tags: [AI, consulting, systems, data, dashboards, organisational-design, methodology, reporting]
source: [[2026-06-05-growify-brain-dump]]
first_seen: 2026-06-05
last_updated: 2026-06-05
content_made: false
content_formats: []
content_pieces: []
---

# Role-Specific Dashboards on a Shared Data Layer

## What It Is

One source of truth at the data layer, then role-specific views layered on top. POCs see their brand metrics. Brand managers see their portfolio. Team leads see team health. Founders see company-level signals. The data is the same everywhere; the context window is different for each role.

## Why It Matters

Most dashboard projects fail because they try to build one view that serves everyone — it ends up too complex for junior staff and too granular for founders, so nobody trusts it. The correct architecture separates the concern: the data layer is shared and consistent, the presentation layer is tailored to the person using it. This is also how AI agents should be designed — one knowledge base, different prompts and contexts per role.

## How to Use It

**As a coach:** When a client complains that their reporting system isn't working, ask: who needs to see what, and is the same view serving multiple different needs? The fix is usually decomposition, not redesign.

**As a consultant:** This is the architecture spec for any multi-stakeholder reporting project. Define the roles, define what each role needs to act on, then build the views. The shared data layer is the non-negotiable foundation.

**As a content creator:** The reason your team ignores the dashboard isn't the data — it's that the dashboard isn't for them.

## Content Angles

- One dashboard for all users is a dashboard for no users.
- The data layer should be shared; the context window should be personal.
- When information architecture fails, the instinct is to add more information — the fix is usually to separate the audiences.

## Seen In

- [[2026-06-05-growify-brain-dump]] — Surfaced at Growify as the correct architecture for client reporting: POCs see their brand, brand managers see their portfolio, team leads see team health, founders see company signals. Same underlying data, role-specific context.
