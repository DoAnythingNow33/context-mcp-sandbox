---
name: AI-Information Proximity
type: principle
tags: [AI, consulting, systems, methodology, architecture, context, performance, design]
source: [[2026-06-13-growify-session-1]]
first_seen: 2026-06-13
last_updated: 2026-06-13
content_made: false
content_formats: []
content_pieces: []
---

# AI-Information Proximity

## What It Is

The effectiveness of an AI agent is directly proportional to how close it is to the information it needs. A local text file is nearly zero distance — the AI reads it instantly, completely, without transformation. A remote dashboard behind an API is many steps away — authentication, data fetch, format translation, context injection. Each step is a point of failure, latency, and information loss.

The design principle: minimise the distance between the AI and the information it needs to act.

## Why It Matters

Most AI implementations fail not because the AI is bad, but because the information is far away. It's locked in a dashboard the AI can't access, a proprietary format it can't parse, or a system that requires a human intermediary to extract and paste. The AI is capable; the information architecture is the bottleneck.

Context folders solve this for workflow knowledge: plain markdown files are zero-distance from any AI model. PostHog's API solves it for analytics: a queryable endpoint the AI can hit directly. The architectural goal is to reduce every layer of indirection between what the AI needs to know and where that information lives.

## How to Use It

**As a coach:** When a client says "I tried using AI for X but it didn't work," ask: where was the information the AI needed? If the answer involves logging into a dashboard and copying things across, you've found the problem.

**As a consultant:** Every ops build should include a proximity audit. For each piece of information the AI might need: how many steps does it take for the AI to get it? Each step above zero is a design problem to solve.

**As a content creator:** The AI isn't the bottleneck. The distance between the AI and your data is.

## Content Angles

- Most AI tools fail because the information they need is three logins and two copy-pastes away.
- The closer your AI is to your information, the smarter it appears. You're not upgrading the model — you're reducing the distance.
- A local text file is the fastest data source your AI will ever have. That's why the context folder matters.

## Seen In

- [[2026-06-13-growify-session-1]] — Named as the design principle behind choosing a context folder over a remote dashboard as the AI's primary knowledge source. The session framed the entire three-layer architecture around this: reduce the distance between AI and information at each layer to maximise agent effectiveness.
