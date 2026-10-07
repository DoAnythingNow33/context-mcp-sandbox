---
description: "Weekly full-auto vault maintenance — reads `_health.md`, heals what's mechanical, decides what's reasonable, and turns anything it can't resolve into an interview for Dan. Designed to run inside /weekly-review or standalone."
---

# /maintain — Full-Auto Vault Maintenance

This skill runs a deterministic health pass and heals the vault. It does not browse. It does not summarise for fun. It reads `_health.md`, fixes what it can, and turns everything it *can't* resolve alone into a short interview Dan answers — then applies his answers on the next run.

> Full-auto means it heals what's mechanical and decides what's reasonable. Anything left needs Dan's judgment, so it becomes an interview question with a built-in resolution — never a passive note that rots in a log.

Designed to run weekly (folded into `/weekly-review`). `scripts/system_health.py` also runs nightly via `evening-debrief.yml` — `/maintain` always regenerates a fresh report before acting.

**There is no health score.** It was retired 2026-08-25: because the daily-log gap carried the biggest penalty, the number mostly measured how diligently Dan fed the vault rather than how useful the vault was to him. Never compute, quote, or invent one, and never grade the week. Surface what's drifting and let him decide what matters.

The loop: **resume open interview → repair → write a new interview for the leftovers.** Over weeks the interview shrinks as Dan's answers teach the skill how he wants recurring calls handled.

---

## Step 0 — Resume any open interview

Before anything else, check for an unresolved interview from a previous run:

```
calendar/[year]/[quarter]/_maintenance-interview.md
```

If it exists, read it. For every question with a filled-in **Your answer:** line, execute the resolution that question maps to (each question carries its own "Resolution if …" mapping — follow it exactly; this is what makes the apply step deterministic). Log each applied resolution in the changelog (Step 4) under "Applied from interview."

Then **archive** it: rename to `_maintenance-interview-answered-DD-MM-YY.md` (today's date) so the next run starts clean and the answers stay on record. Carry forward any question Dan left blank into the new interview you build in Step 5 — an unanswered question is still unresolved.

If no interview file exists, or it's fully blank, skip to Step 1.

---

## Step 1 — Refresh and load

Run the health script first. Never act on a cached report.

```bash
python scripts/system_health.py
```

If the script errors or `_health.md` is not present after running, stop immediately and tell Dan: "system_health.py failed — check the script before running /maintain."

Read `_health.md`. Note `generated` and every tagged finding (`[category.type]` prefixes). Sections are `## GOING QUIET`, `## LOOSE ENDS`, `## VAULT MECHANICS`.

**Token-efficiency contract:** read ONLY `_health.md` plus the specific files named in the findings you are about to act on. Do not open entity files, DPLs, or the IP index unless a finding points at them by path. This is not a reading session — it is a repair session.

---

## Step 2 — Auto-fix (mechanical, no judgment needed)

Do these without asking. Log every change in the Step 4 changelog.

### [cohere.index_drift]
For each drifted row: open `index.md` and rewrite the entity's date column to match `last_updated` in its snapshot frontmatter. Fix all in one pass.

### Misfiled action items — RETIRED
There is no kanban to misfile into. Actions moved to the Notion Tasks Tracker on
2026-09-02; `actions/done/` and `actions/cancelled/` are a frozen archive. Never
move, rewrite, or add files there.

### [cohere.unused_ip]
For each IP entry flagged `content_made: false` and older than 30 days: append a line to `ops/content/_idea-queue.md` (create if missing):

```
- [[IP/<slug>]] — unused IP (Nd), queued YYYY-MM-DD by /maintain
```

Don't draft content — this is a pointer for `/written-content`.

### Digest refresh
After all auto-fixes: run `python scripts/generate_digest.py` to regenerate `_digest.md`.

---

## Step 3 — Act with judgment (resolve if confident; else → interview)

Each item below: if you can make the call confidently from loaded context, make it and log the reasoning. If you can't — or the call is genuinely Dan's — **add it to the interview queue** for Step 5 (do not act). When in doubt, queue it. Never guess on something expensive or irreversible.

### Unfiled next_actions — YOU OWN THIS CHECK NOW

`system_health.py` used to flag these but can't any more: it's offline pure-stdlib
and the actions live in Notion. You have Notion access, so you do it.

Query the Tasks Tracker for every live row (`Status` not `Done`/`Cancelled`),
collecting `Task name` and `Vault Slug`. Then walk each snapshot's `next_actions`
and compare.

**Stale-snapshot guard first.** A snapshot's `next_actions` are only worth filing
if the snapshot is current:

- **Snapshot >21 days stale** → do NOT file its next_actions. They're probably old
  fragments, some already done. Queue ONE interview item: "Snapshot `<path>` is Nd
  stale — refresh it (its next_actions are unreliable until you do)." Skip the rest.
- **Snapshot current (≤21d)** → for each next_action, skip it if a live Notion row
  already covers it (loose title match — don't double-file). Otherwise create a row
  via `notion-create-pages` in data source `1e64c614-f809-80b6-944a-000b9e6dfad4`:
  `Task name` = the next_action text, `Status` = `Backlog`, `Owner` = the entity's
  person or `Daniel`, `Vault Slug` = a fresh kebab slug, `Vault Source` = wikilink
  to the entity file, and `Clients ` = the client page URL when there is one.

### Rotting / stale actions — NOW A NOTION VIEW

`system_health.py` no longer scans these; sort the Tasks Tracker's **Active** view
by last-edited instead. Judge only what's genuinely gone cold, and act in Notion:

- **Still relevant** → leave it. Append a dated line to the page body noting you
  checked, so the next run doesn't re-litigate it.
- **Obviously obsolete** (superseded, the date passed, evidence it's done) → set
  `Status` to `Done` (or `Cancelled` if it was abandoned rather than completed) and
  append a line saying why.
- **Unclear / Dan's call** → leave it and queue: "Action `<Task name>` (Nd untouched)
  — still live, or drop it?"

Anything sitting in `Today`/`This Week` for weeks isn't in progress — it's stalled.
Move it back to `Backlog` rather than leaving the status lying.

### [decay.dpl_gap] / [acct.ratio] — RETIRED
Both checks were removed 2026-08-25. They graded Dan's habits rather than
supporting his work: eight consecutive runs asked about the same unlogged
fortnight while he was doing family-first weeks with a baby due. If you see
these tags in an old report, ignore them. Never re-queue them, and never ask
about daily-log gaps or backlog throughput ratios.

### [cohere.missing_tension]
If the snapshot's `current_state` clearly implies a tension → add one factual bullet lifted from existing language, log it. If nothing implies one → log "no tension apparent — skipped." Don't invent friction, and don't queue this one (it's low-value).

### [cohere.orphan_meeting]
If the entity + month are unambiguous from the filename → add the `[[meeting-stem]]` wikilink to both the entity and month `## Meetings` sections, log it. If ambiguous → queue: "Meeting `<stem>` has no backlinks — which entity/month does it belong to?"

---

## Step 4 — Write the changelog

Determine year/quarter from today. Write or append to:

```
calendar/[year]/[quarter]/_maintenance-log.md
```

Create if missing. Each run appends one block:

```markdown
## YYYY-MM-DD — /maintain
**Open items: <N>** (going quiet <n> · loose ends <n> · mechanics <n>)

### Applied from interview
- <resolution executed + which file> — (omit section if no interview was resumed)

### Auto-fixed
- <what + which file path>

### Acted (judgment)
- <what + why + which file path>

### Queued for interview
- <one line per question written to _maintenance-interview.md>
```

Every file the skill touched appears here. "Acted" entries include the one-line reason. If a section is empty, write "Nothing." rather than dropping it.

---

## Step 5 — Build the interview

Write every queued item (from Step 3, plus any blanks carried forward in Step 0) to:

```
calendar/[year]/[quarter]/_maintenance-interview.md
```

If there are zero queued items, do not create the file — say so and skip to Step 6.

Each item is a self-contained question that carries its own resolution mapping, so the next run's Step 0 can apply Dan's answer deterministically:

```markdown
---
type: maintenance-interview
generated: YYYY-MM-DD
open_questions: <N>
---

# Maintenance Interview — YYYY-MM-DD

Answer the **Your answer:** lines (a letter, or free text). Next `/maintain` run applies them, then archives this file. Skip any you're unsure of — they carry forward.

## Q1 — [tag] <short subject>
**Context:** <one line, grounded in the finding>
**The call:** <the specific decision only Dan can make>
**Options:**
- A) <option> → *Resolution:* <exactly what /maintain will do>
- B) <option> → *Resolution:* <exactly what /maintain will do>
- C) <option> → *Resolution:* <…>
**Your answer:** 

## Q2 — …
```

Order questions by cost of leaving them unresolved — most expensive first (lead with stale snapshots and dead-vs-alive engagement calls, not formatting). Keep each question to the few options that are actually live. Every option must name a concrete resolution — no option should resolve to "discuss later."

---

## Step 6 — Brief Dan, offer to do the interview now

Finish with a 3–5 line console summary: count auto-fixed, count acted, and **the number of open interview questions with the single most expensive one named**. Point Dan at `_maintenance-interview.md`. No score, no trend, no grade.

Then offer: *"Want to run the interview now?"* If yes and you're in an interactive session, walk him through the questions with the `AskUserQuestion` tool (one or a few at a time, most expensive first), apply each answer immediately, log it under "Applied from interview," and archive the interview file at the end. If he'd rather do it later, leave the file for the next run's Step 0.

This is a briefing, not a list. Name the pattern, name what needs his call. Write it as support, not a report card — if a week was quiet because life was busy, say so plainly rather than framing it as a shortfall.

---

## Rules

- Read `_health.md` first, every time. Never act on a report older than 24 hours — regenerate.
- Only read the files the findings name. Token efficiency is a first-class constraint, not a preference.
- Anything you can't resolve yourself becomes an interview question with a built-in resolution — never a dead note. The interview is Dan's review-and-resolve surface; the changelog is the record.
- Every file change goes in the changelog. No silent edits.
- Stale snapshots (>21d) poison their own next_actions — never file from them, always queue the refresh.
- Frontmatter status is the source of truth for action file placement. Reconcile by moving the file.
- Apply the global anti-slop writing rules in any text written into entity, action, or interview files.
- Do not commit. Do not push. Do not run `/wrap` — that's Dan's call at session close.
