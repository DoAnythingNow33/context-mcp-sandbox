---
description: "Content engine — pulls unused IP, weekly review, and audience profile to generate 8 post ideas. Dan picks; engine drafts 4 LinkedIn posts and 7 X tweets in his voice, saved to ops/content/."
---

# /written-content — Content Engine

Turns IP and weekly output into ready-to-post content across LinkedIn and X. Run after the weekly review is written, or any time there's a session to convert into content.

---

## Step 1 — Load source material (all in parallel)

In a single parallel tool call, read:

- The most recent weekly review — find it in `calendar/[year]/[quarter]/weekly/` as the latest `R-DD-MM-YY.md`
- `self/writing-dna.md`
- `self/goals.md`
- `ops/content/linkedin-audience.md`
- `IP/_index.md` — scan for entries where `content_made: false`; these are the primary content source

If no weekly review exists, read the daily logs from the past 7 days in parallel instead.

After reading, note which IP entries have `content_made: false` — list them. These are the raw material that hasn't been used yet. Prioritise them when generating ideas.

---

## Step 2 — Generate 8 post ideas

Generate exactly 8. For each:

- **Number** (1–8)
- **Hook** — the first line of the post. One short sentence. Names a tension, contradiction, or uncomfortable truth. Never starts with "Today I want to talk about..."
- **Premise** — one sentence. What the post is actually about beneath the hook.
- **Emotional target** — one of: *Seen*, *Equipped*, or *Confident* (from linkedin-audience.md)
- **Theme tag** — which of Dan's recurring themes it draws from: identity, decisions, AI, conviction/noise, vision vs. reality, fatherhood as mirror, business + spirituality
- **IP source** — which `IP/_index.md` entry it draws from, if any (write the slug; leave blank if drawn from weekly events only)

Angle guidance:

- Bias toward polarising and emotionally-resonant. The target reader is a founder under real pressure. A post that makes them nod slowly or feel a small sting is better than one they scroll past.
- Use the content lens from linkedin-audience.md: hidden costs of common habits, the decision framework nobody names, honest "I got this wrong," contrarian takes on what founders optimise for, what scaling actually exposes, AI applied to a real business problem.
- Spread across: wins, failures/gaps, principles, personal arc. Not 8 win posts. Not 8 AI posts.
- If there are IP entries with `content_made: false`, pull from them first — they're the unused raw material.

Present all 8 clearly numbered. Then ask:

**"Pick which become LinkedIn posts (aim for 4) and which seed X tweets. I'll draft 4 LinkedIn + 7 tweets in one pass."**

Wait for Dan's selection before proceeding.

---

## Step 3 — Draft in parallel (one pass)

Draft all selected content simultaneously — LinkedIn posts and X tweets in the same parallel tool call.

### LinkedIn posts

Each post follows the structural pattern from `writing-dna.md`:

1. **Hook** — one short line naming the tension or contradiction
2. **Setup** — 2–4 short lines of personal context
3. **The turn** — what was caught, revealed, or shifted
4. **The principle** — what this means, said plainly in one line
5. **Close** — the contrast between most people and the alternative; leaves the reader somewhere

Voice rules (non-negotiable):
- Short sentences. Often fragments. White space is part of the voice.
- No buzzwords. No hustle-culture language. No qualifiers softening hard truths.
- Does not end on a question — Dan answers his own questions.
- Does not explain the metaphor. Trusts the reader to land it.
- Bold used on the single word that carries the weight.
- Run the TED-Talk AI Slop checklist from `writing-dna.md` on every draft before finalising.

Audience rules:
- Write for a founder under real pressure — match that register, don't soften it.
- Name their private experience before they've named it themselves.
- Every post leaves them *Seen*, *Equipped*, or *Confident*. If it doesn't do one of those three, the draft isn't done.
- Credibility comes from specificity, not credentials. Name the actual thing.

Format each LinkedIn post as:

---
**Post [N] — [Hook as title]**
*Suggested day: [Monday / Tuesday / Wednesday / Thursday]*
*Theme: [tag]*
*IP source: [slug or "weekly events"]*

[Full post body — copy-paste ready]

*Check before posting: [one specific thing to verify — client name, stat, claim]*

---

### X tweets

7 tweets total. Each one is standalone — one idea, one punch. They can be derived from the same idea pool as the LinkedIn posts, but they're not excerpts. They work differently: shorter, more blunt, sometimes more irreverent.

Format each tweet as:

**Tweet [N]**
[Tweet body — max 280 characters, no hashtags unless genuinely earned]
*IP source: [slug or blank]*

---

## Step 4 — Save drafts (parallel)

Save all files in a single parallel tool call.

**LinkedIn posts** — one file per post:

Path: `ops/content/linkedin/Deferred/YYYY-MM-DD-[slug].md`
- `YYYY-MM-DD` = today's date
- `[slug]` = 3–4 words from the hook, lowercase, hyphens
- New drafts start in `Deferred/` — Dan moves them to `Posted/` manually when posted

Frontmatter:
```yaml
---
title: [hook line]
type: content
platform: linkedin
status: deferred
date: YYYY-MM-DD
ip_sources: []
---
```

**X tweets** — one combined file:

Path: `ops/content/x/Deferred/YYYY-MM-DD-tweets.md`

Frontmatter:
```yaml
---
type: content
platform: x
status: deferred
date: YYYY-MM-DD
ip_sources: []
---
```

Body: all 7 tweets numbered and copy-paste ready.

---

## Step 5 — IP source tracking

For any IP entry used as a source, note it clearly after saving:

**"These IP entries were used — `content_made` is still `false` on each. When you post the content, update the entry to `content_made: true` and add the file to `content_pieces`. Want me to flip any of them now?"**

Wait for Dan's answer. Only update IP entries if he confirms.

---

## Step 6 — Confirm

After saving:

**"Done. [N] LinkedIn drafts in `ops/content/linkedin/Deferred/`, 7 tweets in `ops/content/x/Deferred/`. Edit, post, move to Posted/ when live. Anything to change?"**

That's it. No coaching. No follow-up suggestions beyond the check note per post.

---

## Rules

- Always generate exactly 8 ideas in Step 2 — not 6, not 10.
- Never draft before Dan picks — wait for his selection.
- Draft all content in a single parallel pass — not sequentially.
- Save all files before confirming — always.
- Never use Dan's clients' names in post drafts without a check note flagging it.
- If source material is thin (short week, no review file, no unused IP), say so before generating ideas — don't pad to compensate.
- The `content_made: true` flip happens when Dan posts, not when the draft is saved. Make this distinction explicit.
