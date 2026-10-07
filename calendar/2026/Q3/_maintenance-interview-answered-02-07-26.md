---
type: maintenance-interview
generated: 2026-07-02
open_questions: 7
---

# Maintenance Interview — 2026-07-02

Answer the **Your answer:** lines (a letter, or free text). Next `/maintain` run applies them, then archives this file. Skip any you're unsure of — they carry forward.

## Q1 — [decay.dpl_gap] Missing daily logs
**Context:** 7 of the last 14 days have no DPL: 2026-06-24, 2026-06-25, 2026-06-27, 2026-06-28, 2026-06-29, 2026-07-01, 2026-07-02. This is the single biggest lever on the health score right now.
**The call:** Backfill what you can from memory, or accept the gap and move forward logging only from today.
**Options:**
- A) I'll backfill the days I have data for → *Resolution:* /maintain will ask for details on each date next run and write minimal DPL entries from what you provide.
- B) Let them go, just log going forward → *Resolution:* /maintain notes the gap as accepted in the changelog and doesn't chase it again.
**Your answer:**

## Q2 — [decay.parked_thread] Content engine — identity sentence decision
**Context:** LinkedIn and Instagram have been stalled 3+ weeks. Per `self/goals.md`, the root cause is identity confusion between the two-track model. The unresolved decision is spelled out in `actions/backlog/2026-06-26-three-initiatives-next-steps.md` — "What is DoAnythingNow in one sentence?"
**The call:** Only you can write that sentence — it's the blocker for restarting content.
**Options:**
- A) I have the sentence: (write it in your answer) → *Resolution:* /maintain writes it into `self/identity.md` and `self/goals.md`, and updates the parked-thread entry to reflect content is unblocked.
- B) Not ready yet, keep it parked → *Resolution:* /maintain leaves the thread parked and re-queues this question next run.
**Your answer:**

## Q3 — [decay.quiet_entity / acct.unfiled_next_action] Family — stale snapshot
**Context:** Family snapshot hasn't been updated since 2026-04-13 (80 days), no meetings logged. A generic check-in action was filed (`check-in-family.md`) since none existed, but the snapshot's next_actions weren't filed — too old to trust, especially with the baby due end of August.
**The call:** Refresh the snapshot, or confirm it's still accurate as-is.
**Options:**
- A) Refresh it — here's what's current: (write it in your answer) → *Resolution:* /maintain updates `entities/people/family.md`'s current_state/next_actions from what you provide and files any genuinely new next_actions.
- B) Still accurate, just quiet → *Resolution:* /maintain bumps `last_updated` to today without changing content, and files the existing next_actions (childcare conversation, date night, August household prep).
**Your answer:**

## Q4 — [decay.quiet_entity] Santiago / Bonita — alive or dead?
**Context:** No meetings ever logged for this entity. Snapshot 66d stale (`last_updated: 2026-04-27`). No open action currently exists for it.
**The call:** Is the Santiago/Bonita creative-arm partnership still active, or has it quietly ended?
**Options:**
- A) Still active, just informal → *Resolution:* /maintain refreshes the snapshot's `last_updated` and files its next_actions (Define Instagram content series, Formalise equity agreement, Build brand list) as backlog actions.
- B) Stalled/dead → *Resolution:* /maintain adds a tension noting the engagement may be over and leaves next_actions unfiled until you confirm next steps.
**Your answer:**

## Q5 — [decay.rotting_action / decay.quiet_entity] Fadwa — overdue June items
**Context:** Fadwa's snapshot is 37d stale (no meeting since 2026-05-26). Two backlog actions are now past due: `fadwa-send-june-session-dates.md` (waiting on Fadwa) and `send-fadwa-white-paper.md` (waiting on your edit) — both were due before end of June.
**The call:** Chase Fadwa for session dates, and confirm whether the white paper edit is actually done.
**Options:**
- A) I'll chase Fadwa this week → *Resolution:* /maintain leaves both actions in place, re-stamps them as still relevant/waiting.
- B) White paper edit is done, ready to send → *Resolution:* /maintain moves `send-fadwa-white-paper.md` to `doing/` with `status: doing`.
- C) Drop the June session, reschedule for the next window → *Resolution:* /maintain moves `fadwa-send-june-session-dates.md` to `done/` with a dropped note, and files a new backlog action for the next session window.
**Your answer:**

## Q6 — [decay.quiet_entity / acct.unfiled_next_action] Shereen — stale snapshot
**Context:** Shereen/Bubble Balloon Heaven snapshot is 39d stale (`last_updated: 2026-05-24`). An open action already exists (`shereen-confirm-scope.md`), but her next_action "Deliver the 5 hours" wasn't filed since the snapshot is too old to trust.
**The call:** Has scope been confirmed since the snapshot was last touched?
**Options:**
- A) Still waiting on her to confirm scope → *Resolution:* /maintain bumps `last_updated` to today, leaves next_actions unfiled.
- B) Scope confirmed, ready to deliver → *Resolution:* /maintain files "Deliver the 5 hours" as a new backlog action and updates the snapshot's current_state.
**Your answer:**

## Q7 — [cohere.orphan_meeting] 2025-06-05-growify-ontology — date looks off
**Context:** This meeting file is dated 2025-06-05 — a full year before the vault existed and before the Growify proposal was even accepted (2026-05-10). It closely mirrors `2026-06-05-growify-brain-dump` (same day-of-month, one year later, similar content). It links to `entities/people/growify` but has no reverse link, and no calendar month exists for 2025-06.
**The call:** Is 2025-06-05 correct, or is this a typo for 2026-06-05?
**Options:**
- A) It's a typo, should be 2026-06-05 → *Resolution:* /maintain renames the file and its `date` frontmatter to `2026-06-05-growify-ontology.md`, and links it from `entities/people/growify.md` and the June 2026 calendar month file.
- B) 2025-06-05 is correct (pre-engagement context) → *Resolution:* /maintain links it from `entities/people/growify.md` only (no calendar month exists for that period).
**Your answer:**
