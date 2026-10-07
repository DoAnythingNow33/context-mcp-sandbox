---
name: Keep the Agent Light
type: principle
tags: [AI, consulting, systems, architecture, performance, Hermes, methodology, design]
source: [[2026-06-29-growify-session-2]]
first_seen: 2026-06-29
last_updated: 2026-06-29
content_made: false
content_formats: []
content_pieces: []
---

# Keep the Agent Light

## What It Is

The always-on AI assistant should hold only personality and memory of the user — not business context. Business context lives in a separate folder. The agent navigates to that folder via routing when it needs information, rather than carrying everything in its own system prompt.

## Why It Matters

Loading business context into the agent's system prompt causes token bloat, slower responses, and a maintenance nightmare — every time the business changes, you're editing the agent itself. Keeping the agent light means context is updated in one place (the folder), the agent stays fast and cheap, and the architecture scales. The agent is the bridge; the folder is the brain.

## How to Use It

**As a coach:** Frame it as a division of responsibility: the agent holds the relationship (who you are, how you communicate), the folder holds the knowledge (what's happening, what matters). This maps naturally onto how good human assistants work.

**As a consultant:** Applies directly to always-on assistant setups (Hermes-style). The design principle: agent system prompt = personality + routing instructions only. All substantive context = files the agent reads on demand. Keeps the system auditable and maintainable.

**As a content creator:** The counterintuitive angle: the smarter you want your AI to be, the less you should put in it. The intelligence is in the folder, not the agent.

## Content Angles

- Most people try to make the agent smarter by giving it more context upfront. This principle says the opposite: give it less, and point it to where the context lives.
- The question: "Is your AI fast because it's smart, or slow because it's carrying too much?"
- Story: an always-on assistant that starts fast and gets slower and more expensive as more context is loaded in — versus the folder-routing model that stays lean at any scale.

## Seen In

- [[2026-06-29-growify-session-2]] — came up while designing Growify's always-on assistant architecture; the separation of agent personality from business context was named as a design principle
