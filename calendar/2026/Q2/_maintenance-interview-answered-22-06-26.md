---
type: maintenance-interview
generated: 2026-06-22
open_questions: 5
---

# Maintenance Interview — 2026-06-22

Answer the **Your answer:** lines (a letter, or free text). The next `/maintain` run applies them, then archives this file. Skip any you're unsure of — they carry forward.

## Q1 — [acct.unfiled_next_action] DoAnythingNow snapshot is 43 days stale
**Context:** `entities/projects/snapshot.md` last updated ~6 weeks ago. Its 6 `next_actions` are old daily-plan fragments — several already done (Modules 2/3/4 posted, Growify invoice sent). /maintain refused to file them as actions.
**The call:** How do you want the stale business snapshot handled?
**Options:**
- A) I'll refresh it myself now → *Resolution:* /maintain re-scans it next run; if current, files any genuinely-open next_actions.
- B) Refresh it for me from recent meetings + goals + DPLs → *Resolution:* /maintain drafts an updated snapshot for your sign-off, then files open next_actions.
- C) Leave it — it's low priority → *Resolution:* /maintain stops flagging it for 30 days.
**Your answer:** 

## Q2 — [decay.quiet_entity] Sam / Explorers Club — 29 days quiet
**Context:** No meeting in 29d; snapshot is a waiting-state ("waiting on Sam to book final meeting + collect payment"). A chase action was filed this run (`explorers-club-chase-sam`).
**The call:** Is this engagement still alive?
**Options:**
- A) Still live, keep chasing → *Resolution:* keep the chase action; no further change.
- B) Probably dead — last chase, then close → *Resolution:* keep the chase action, but if no reply in 14d /maintain queues closing it out + moving the thread to Completed.
- C) Dead now → *Resolution:* move "Sam final meeting" thread to `## Completed` in goals, mark the chase action done with a "closed unpaid/unbooked" note.
**Your answer:** 

## Q3 — [decay.parked_thread] Claude Architect Certificate
**Context:** Parked in goals "until Growify sessions settle." Those sessions ended 21 Jun, so the park condition has now cleared.
**The call:** The blocker's gone — what now?
**Options:**
- A) Give it a named block → *Resolution:* /maintain files a "Block time for Claude Architect Certificate" action and keeps the thread active.
- B) Still not now → *Resolution:* move the thread to `## Someday / Deferred`.
- C) Drop it → *Resolution:* move the thread to `## Completed` as abandoned.
**Your answer:** 

## Q4 — [decay.dpl_gap] 9 of last 14 days unlogged
**Context:** No DPL for Jun 9, 10, 11, 14, 17, 18, 19, 20, 21. This is the single biggest drag on the health score — the system can't hold you accountable for days it has no record of.
**The call:** Backfill any of these?
**Options:**
- A) I'll log the key ones retroactively → *Resolution:* none needed; score recovers as you fill them.
- B) Walk me through them now → *Resolution:* /maintain opens a quick gap-fill, one day at a time, writes the DPLs from your answers.
- C) Skip — gone is gone → *Resolution:* /maintain stops counting these specific dates against the score.
**Your answer:** 

## Q5 — [acct.ratio] Backlog growing faster than it clears
**Context:** Backlog is now 23 items (11 filed this run); commit→done ratio over the last 7d was effectively flat. Nothing is in `doing/`.
**The call:** How do you want to clear it down?
**Options:**
- A) Pull 3 into doing/ now → *Resolution:* tell me which 3 and /maintain moves them to `doing/`.
- B) Block a clear-down session this week → *Resolution:* /maintain files a "Backlog clear-down" action for the deep-work block.
- C) It's fine, leave it → *Resolution:* no change; /maintain won't re-flag the ratio for 14d.
**Your answer:** 
