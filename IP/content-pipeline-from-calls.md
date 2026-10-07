---
name: Content Pipeline from Calls
type: technique
tags: [AI, content, systems, LinkedIn, workflows, coaching]
source: [[2026-05-08-jamie-session-1]]
first_seen: 2026-05-08
last_updated: 2026-05-08
content_made: false
content_formats: []
content_pieces: []
---

# Content Pipeline from Calls

## What It Is

A structured pipeline that turns every recorded call into ready-to-edit content: record call → extract transcript → run `/call-extraction` skill → content bank file → run `/linkedin-posts` skill → draft posts. Each call automatically feeds the content library without any additional effort at the time.

## Why It Matters

The blank-page problem kills content consistency. Most people know they should be creating content from their conversations — the insights are already there — but the friction between "interesting call" and "published post" is high enough that it never happens. This pipeline removes that friction entirely. You do your work, the content follows automatically.

## How to Use It

**As a coach:** Recommend this to any client who says "I don't have time to create content." They're already having the conversations — they just don't have the pipeline. Set up Fathom (or any transcript tool), two Claude Code skills, and a content bank folder. Total setup: one session.

**As a consultant:** Deploy for internal knowledge capture too, not just content. The same pipeline (call → extraction → bank) works for project debriefs, client meetings, and discovery calls — the output just changes from LinkedIn drafts to internal docs or IP entries.

**As a content creator:** This is how consistent creators actually do it. They're not sitting down to "create content" — they're processing their work. The call was the work; the post is a byproduct.

## Content Angles

- "I don't have time to create content" usually means "I don't have a pipeline." You have the conversations. You just don't have the system to extract them.
- The insight that lands: you're not creating content, you're processing it. The content already exists inside the calls you're already having.
- The processed/ subfolder detail — once a content bank file has been used to generate posts, it moves to processed/. Clean, simple, no duplication. That's the kind of small design decision that makes a system feel like it works.

## Seen In

- [[2026-05-08-jamie-session-1]] — Built live with Jamie for Social Trait's LinkedIn operation. Three-skill pipeline: call extraction → tone-of-voice template → LinkedIn post generation. The processed/ folder idea surfaced naturally mid-session as the obvious way to track usage.
