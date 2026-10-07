---
type: maintenance-interview
generated: 2026-07-05
open_questions: 8
---

# Maintenance Interview — 2026-07-05

Answer the **Your answer:** lines (a letter, or free text). Next `/maintain` run applies them, then archives this file. Skip any you're unsure of — they carry forward.

## Q1 — [decay.dpl_gap] Missing daily logs
**Context:** 10 of the last 14 days have no DPL: 2026-06-24, 2026-06-25, 2026-06-27, 2026-06-28, 2026-06-29, 2026-07-01, 2026-07-02, 2026-07-03, 2026-07-04, 2026-07-05. This has grown from 7 missing days three days ago and is still the single biggest lever on the health score.
**The call:** Backfill what you can from memory, or accept the gap and move forward logging only from today.
**Options:**
- A) I'll backfill the days I have data for → *Resolution:* /maintain will ask for details on each date next run and write minimal DPL entries from what you provide.
- B) Let them go, just log going forward → *Resolution:* /maintain notes the gap as accepted in the changelog and doesn't chase it again.
**Your answer:** B) Let them go — it's been a couple of weeks of changes, log fresh from today.

## Q2 — [decay.parked_thread] Content engine — identity sentence decision
**Context:** LinkedIn and Instagram have been stalled 3+ weeks. Per `self/goals.md`, the root cause is identity confusion between the two-track model. The unresolved decision is spelled out in `actions/backlog/2026-06-26-three-initiatives-next-steps.md` — "What is DoAnythingNow in one sentence?" This is also the reason Sleevenote's 5 next_actions and the wider carousel/website work stay unfiled — everything downstream is gated on this one sentence.
**The call:** Only you can write that sentence — it's the blocker for restarting content.
**Options:**
- A) I have the sentence: (write it in your answer) → *Resolution:* /maintain writes it into `self/identity.md` and `self/goals.md`, updates the parked-thread entry to reflect content is unblocked, and files the Sleevenote/website/carousel next_actions that were waiting on it.
- B) Not ready yet, keep it parked → *Resolution:* /maintain leaves the thread parked and re-queues this question next run.
**Your answer:** A) I have the sentence — use the one already resolved in `self/goals.md` (2026-07-08 identity session): "DoAnythingNow helps humans remember the magic of being human again — creativity as the superpower in every part of life."

## Q3 — [decay.quiet_entity / acct.unfiled_next_action] Disha Bhatnagar — return date is today
**Context:** Disha's snapshot (`entities/people/disha.md`) is 30d stale (`last_updated: 2026-06-05`) — over the 21d guard threshold, so her 2 pending next_actions ("Confirm PostHog decision with Disha," "Check whether Rishabh-Disha alignment on manual vs automated reporting has moved") aren't being filed. But the snapshot itself names 2026-07-05 — today — as the date she returns for her second session. Growify's own "Book Disha session" next_action is already covered by the open `growify-second-sessions-rishab-disha.md`, so that part's handled; this question is about the snapshot's freshness, not the booking.
**The call:** Has Disha's second session actually happened or been scheduled since her return?
**Options:**
- A) Not yet — still waiting on scheduling → *Resolution:* /maintain bumps `last_updated` to today, leaves the 2 next_actions unfiled, re-queues this question next run.
- B) Session happened / scheduled — here's what's current: (write it in your answer) → *Resolution:* /maintain updates `entities/people/disha.md`'s current_state/next_actions from what you provide and files any next_actions that are still genuinely open.
**Your answer:** A) Not yet — I need to schedule it with her tomorrow (2026-07-14).

## Q4 — [decay.quiet_entity / acct.unfiled_next_action] Family — stale snapshot
**Context:** Family snapshot hasn't been updated since 2026-04-13 (now 83 days), no meetings logged. All 3 of its listed next_actions ("Speak to parents about fortnightly childcare," "Plan one date night," "Think ahead: household needs before August") already have matching **done** actions filed 2026-06-22 — the snapshot itself was never updated to reflect that, so it keeps surfacing the same stale text every run.
**The call:** Those 3 items look done. Confirm, and/or tell us what's actually current for Family with the baby due end of August.
**Options:**
- A) Refresh it — here's what's current: (write it in your answer) → *Resolution:* /maintain updates `entities/people/family.md`'s current_state/next_actions from what you provide and files any genuinely new next_actions.
- B) The 3 listed items are done, nothing else has changed → *Resolution:* /maintain bumps `last_updated` to today, clears those 3 resolved next_actions, and leaves current_state as-is.
**Your answer:** B) The 3 listed items are done, nothing else has changed — but also: there's a family context folder at `/Users/DoAnythingNow./Desktop/TejadaScottFamily` — document it as a reference in case it's needed.

## Q5 — [decay.quiet_entity] Santiago / Bonita — alive or dead?
**Context:** No meetings ever logged for this entity. Snapshot 69d stale (`last_updated: 2026-04-27`). No open action currently exists for it.
**The call:** Is the Santiago/Bonita creative-arm partnership still active, or has it quietly ended?
**Options:**
- A) Still active, just informal → *Resolution:* /maintain refreshes the snapshot's `last_updated` and files its next_actions (Define Instagram content series, Formalise equity agreement, Build brand list) as backlog actions.
- B) Stalled/dead → *Resolution:* /maintain adds a tension noting the engagement may be over and leaves next_actions unfiled until you confirm next steps.
**Your answer:** B) Stalled/dead — it should be in archive.

## Q6 — [decay.rotting_action / decay.quiet_entity] Fadwa — overdue June items
**Context:** Fadwa's snapshot is 40d stale (no meeting since 2026-05-26). Two backlog actions are now well past due: `fadwa-send-june-session-dates.md` (waiting on Fadwa) and `send-fadwa-white-paper.md` (waiting on your edit) — both were due before end of June. 2 more of her listed next_actions ("Follow up on Circa Arts application / Joseph response," "Define content direction and first pieces to publish") already have matching **done** actions filed 2026-06-22 — same stale-snapshot pattern as Family (Q4).
**The call:** Chase Fadwa for session dates, confirm whether the white paper edit is done, and confirm the snapshot can be refreshed.
**Options:**
- A) I'll chase Fadwa this week → *Resolution:* /maintain leaves both actions in place, re-stamps them as still relevant/waiting.
- B) White paper edit is done, ready to send → *Resolution:* /maintain moves `send-fadwa-white-paper.md` to `doing/` with `status: doing`.
- C) Drop the June session, reschedule for the next window → *Resolution:* /maintain moves `fadwa-send-june-session-dates.md` to `done/` with a dropped note, and files a new backlog action for the next session window.
- D) Also refresh the snapshot — clear the Circa Arts and content-direction items, they're done → *Resolution:* /maintain bumps `last_updated` to today and clears those 2 resolved next_actions from `entities/people/fadwa.md`.
**Your answer:** B) White paper edit is done — already sent. Also: the last session with Fadwa is happening soon, and she's paid the final amount.

## Q7 — [decay.quiet_entity / acct.unfiled_next_action] Shereen — stale snapshot
**Context:** Shereen/Bubble Balloon Heaven snapshot is 42d stale (`last_updated: 2026-05-24`). An open action already exists (`shereen-confirm-scope.md`), but her next_action "Deliver the 5 hours" wasn't filed since the snapshot is too old to trust.
**The call:** Has scope been confirmed since the snapshot was last touched?
**Options:**
- A) Still waiting on her to confirm scope → *Resolution:* /maintain bumps `last_updated` to today, leaves next_actions unfiled.
- B) Scope confirmed, ready to deliver → *Resolution:* /maintain files "Deliver the 5 hours" as a new backlog action and updates the snapshot's current_state.
**Your answer:** A) Still waiting on her — I'm calling her tomorrow (2026-07-14) to confirm what's actually happening.

## Q8 — [cohere.orphan_meeting] 2025-06-05-growify-ontology — date looks off
**Context:** This meeting file is dated 2025-06-05 — a full year before the vault existed and before the Growify proposal was even accepted (2026-05-10). It closely mirrors `2026-06-05-growify-brain-dump` (same day-of-month, one year later, similar content). It links to `entities/people/growify` but has no reverse link, and no calendar month exists for 2025-06.
**The call:** Is 2025-06-05 correct, or is this a typo for 2026-06-05?
**Options:**
- A) It's a typo, should be 2026-06-05 → *Resolution:* /maintain renames the file and its `date` frontmatter to `2026-06-05-growify-ontology.md`, and links it from `entities/people/growify.md` and the June 2026 calendar month file.
- B) 2025-06-05 is correct (pre-engagement context) → *Resolution:* /maintain links it from `entities/people/growify.md` only (no calendar month exists for that period).
**Your answer:** A) It's a typo — confirmed by comparing content against `meetings/2026-06-05-growify-brain-dump.md`: same session (Disha brain-dump, same bottlenecks — image resizing, ad creative backlog, weekly reports, PostHog/Claude architecture), just the fuller ontology-map version. Should be 2026-06-05.
