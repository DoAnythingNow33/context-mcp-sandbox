---
description: "IP extractor — identifies Frameworks, Concepts, Techniques, Principles, Analogies, and Patterns from a transcript or meeting file and writes them to the IP library."
---

# /pull-ip — IP Extractor

Reads a transcript (or an existing meeting file) and files what belongs in the IP library. Runs as Agent 1 inside `/meeting`, or standalone whenever Dan wants to mine a transcript or note for reusable knowledge.

---

## Mode detection

**Orchestrated (called by `/meeting`):** The transcript, meeting file path, entity name, and date are passed in. Skip Steps 1–2 — go straight to Step 3. Write confirmed entries directly (no confirm gate). Report counts back to the orchestrator.

**Standalone:** Run Steps 1–2 first.

---

## Step 1 — Get the source (standalone only)

Ask Dan:

- **Paste a transcript** — or —
- **Give a meeting file path** (e.g. `meetings/2026-05-24-growify-call.md`) and Dan pastes the transcript from there, or you read the file.

If a meeting file path is given, read the file and use its transcript / Key Discussion content as the source material. Note the meeting file path so it can be set as `source` in each entry.

---

## Step 2 — Read the index (standalone only)

Read `IP/_index.md`. This is the only upfront read needed — it lets Step 3 cross-reference without reading the full library.

(When orchestrated, assume `IP/_index.md` was already read by the orchestrator or read it now if not passed in.)

---

## Step 3 — Extract IP candidates

Scan the transcript for anything worth a standalone IP entry. The bar is: **would Dan reach for this in a future coaching session, consulting engagement, or content piece?**

Categories to look for:

| Category | What qualifies |
|----------|---------------|
| **Framework** | A repeatable structure for diagnosing or doing something |
| **Concept** | A named idea that reframes how something is understood |
| **Technique** | A specific method or practice — executable steps |
| **Principle** | A transferable truth about how people or systems behave |
| **Analogy** | A comparison that makes something abstract land |
| **Pattern** | A recurring dynamic across clients, organisations, or conversations |

Be opinionated. Flag the 2–4 strongest candidates, not every noun. If something barely qualifies, leave it out. A mediocre IP entry degrades the library.

---

## Step 4 — Cross-reference the index

For each candidate:

- **Already in `IP/_index.md`** → flag as an **update candidate**. State which existing entry it maps to and what the new occurrence adds. Do not auto-update the existing file.
- **Not in `IP/_index.md`** → mark as **new entry**. Prepare the full entry from the schema below.

---

## Step 5 — Present and confirm (standalone only)

Show Dan a brief list:

**"[N] new IP entries ready to file: [Name 1], [Name 2], ... [M] existing entries that could be updated: [Name] → maps to [[existing-entry]]. Confirm to write new entries, or tell me which to skip."**

Wait for Dan's response before writing anything.

(When orchestrated, skip this step — write directly and report.)

---

## Step 6 — Write entries

For each confirmed new entry, write `IP/<slug>.md` using this schema (from `IP/_template.md`):

```yaml
---
name: [Name]
type: concept | tool | technique | framework | principle | analogy
tags: [relevant tags]
source: [[YYYY-MM-DD-entity-descriptor]]
first_seen: YYYY-MM-DD
last_updated: YYYY-MM-DD
content_made: false
content_formats: []
content_pieces: []
---
```

Body sections — write all of them, not stubs:

**## What It Is** — 1–2 sentences, plain language. No jargon unless the jargon is the point.

**## Why It Matters** — The core insight. Write it as a claim you'd defend, not a description.

**## How to Use It**
- **As a coach:** How this shows up in 1:1 work — what it helps a client see or shift.
- **As a consultant:** How this applies in an engagement — what it diagnoses, builds, or delivers.
- **As a content creator:** The angles, the hooks, the post this wants to become.

**## Content Angles**
- The tension or contradiction this creates — what most people believe vs. what's true.
- The question this answers that people don't know how to ask.
- The story that demonstrates it.

**## Seen In**
- `[[YYYY-MM-DD-source]]` — one-line context: where it came up and how it landed.

In the same parallel tool call, append one row per new entry to `IP/_index.md`:

```
| [Name] | [type] | [tags, comma-separated] | YYYY-MM-DD | [[slug]] |
```

---

## Step 7 — Report

**Standalone:** "Done. [N] IP entries written: [Name 1] ([[slug-1]]), [Name 2] ([[slug-2]]). [M] existing entries flagged for review: [list]. No existing entries were auto-updated."

**Orchestrated:** Return counts to the orchestrator — new entries written, slugs, existing entries flagged.

---

## Rules

- Quality bar: use existing `IP/` entries as the standard. If you can't write a full entry with what the transcript gives you, write what you have and flag the gaps inline in the file.
- `source` field must point to the meeting file wikilink, not the entity.
- `first_seen` = meeting date. `last_updated` = same on creation.
- Never auto-update an existing IP entry. Flag it — Dan decides.
- Slug = lowercase kebab of the concept name. Keep it short. No dates in the slug.
- Do not re-read files after writing to verify.
- If `IP/_index.md` cannot be found, stop and tell Dan before writing any entries.
