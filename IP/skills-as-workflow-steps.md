---
name: Skills-as-Workflow-Steps
type: framework
tags: [AI, Claude Code, systems, workflows, methodology]
source: [[2026-05-08-jamie-session-1]]
first_seen: 2026-05-08
last_updated: 2026-05-08
content_made: false
content_formats: []
content_pieces: []
---

# Skills-as-Workflow-Steps

## What It Is

Each atomic action in a workflow is its own skill — a single-purpose prompt with one job. A full workflow is a pipeline of skills chained together, not one monolithic prompt trying to do everything.

## Why It Matters

When people first use AI for workflows they try to build one giant prompt that does everything. It breaks, it's unmaintainable, and when something goes wrong you can't diagnose where. Breaking it into discrete skills means each step is testable, replaceable, and composable — and you can improve one step without touching the others.

## How to Use It

**As a coach:** When a client describes a complex task they want AI to handle, ask them to break it into steps first. Each step that requires different context or produces a distinct output is its own skill. The goal is one job per skill.

**As a consultant:** Use this framework to map a client's workflow before writing any prompts. Draw the pipeline: input → skill 1 → output → skill 2 → output → skill 3 → final output. Build left to right, test each node independently.

**As a content creator:** This is the counter-narrative to "just ask ChatGPT." Sophisticated AI use isn't one clever prompt — it's architecture. The people getting real leverage have pipelines, not prompts.

## Content Angles

- Most people build one fat prompt and wonder why it breaks. The real move is to think like a software engineer: one function, one job.
- The question people don't know to ask: "Where does this step end and the next one begin?" Answering that is 80% of workflow design.
- The meal planner demo: three skills (choose meals / generate list / format for shopping app), each simple, combined into something genuinely useful. The magic isn't in any one skill — it's the chain.

## Seen In

- [[2026-05-08-jamie-session-1]] — Taught live while building Jamie's content pipeline; framed explicitly as "each step is a skill, your workflow is a bunch of skills." It landed and shaped how he approached the rest of the session.
