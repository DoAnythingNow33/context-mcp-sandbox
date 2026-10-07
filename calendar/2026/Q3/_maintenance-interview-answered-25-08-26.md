---
type: maintenance-interview
generated: 2026-08-25
open_questions: 7
---

# Maintenance Interview — 2026-08-25

Answer the **Your answer:** lines (a letter, or free text). Next `/maintain` run applies them, then archives this file. Skip any you're unsure of — they carry forward.

> **2026-08-25:** the daily-log-gap and commit→done-ratio questions were removed from this interview and retired from `system_health.py`. They graded habits rather than supporting work. Remaining questions are all real calls only Dan can make.

## Q1 — [decay.rotting_action] Soho Spirits Festival (21-22 Aug) — did it happen, and are the prep actions moot?
**Context:** Four Victoria-partnership actions from the 2026-08-07 session — `dan-intro-victoria-nothing-headphones` (headphone loan), `victoria-dm-tom-sleevenote-festival` (device request + site visit), `victoria-email-anthony-vinyl-factory-visit` (Phonica site visit), `victoria-text-tony-calabasa-booth` (booth slot ask) — were all built around the Soho Spirits Festival, 21–22 Aug. That date has now passed, but Victoria's snapshot was last updated 2026-08-11 (pre-festival) and hasn't been refreshed with what actually happened. Her 2026-08-11 snapshot already flagged that Sleevenote was likely dropping out in favor of her own backup device partner, so some of these may already be moot.
**The call:** Did the festival happen, and which (if any) of these four are still live vs. superseded by the outcome?
**Options:**
- A) Festival happened, all four are done/moot now → *Resolution:* /maintain moves all four to `done/` with a dropped note (festival passed), and queues a snapshot-refresh note for Victoria's entity file.
- B) Festival happened, some are still relevant (e.g. follow-up thank-yous, booth outcome) → *Resolution:* free-text which ones stay live; /maintain drops the rest to `done/` and leaves the named ones in backlog with an updated note.
- C) Festival didn't happen / was postponed → *Resolution:* /maintain leaves all four in backlog, annotates with the postponement, and won't re-flag as rotting for 14 days.
**Your answer:** Festival happened, but Dan hasn't caught up on the outcome. All four prep actions dropped as time-expired; replaced with a single catch-up action (victoria-catchup-festival-outcome) covering the booth, Phonica, Tom/Sleevenote threads and a snapshot refresh.
## Q2 — [acct.unfiled_next_action] Ontology for Creatives — snapshot is 27 days stale
**Context:** This new-direction snapshot (surfaced 2026-07-29) still hasn't been touched — now 27 days, further past the 21-day staleness guard. It carries two unfiled next_actions ("add detail on the conversation that sparked this," "draft what a Roundhouse-style workshop pitch would contain") that weren't filed this run because the snapshot itself is unreliable until refreshed. No open action exists for this entity yet. Carried forward a third run.
**The call:** Is this thread still live and worth a snapshot refresh + filing its next_actions, or has it gone quiet because it's been deprioritised behind Mycelium/Growify/Sleevenote?
**Options:**
- A) Still live, refresh it → *Resolution:* /maintain files both next_actions to `actions/backlog/` on your confirmation and treats the snapshot as current again (you'll want to actually update `current_state`/`last_updated` yourself, or in the next session).
- B) Deprioritised for now, leave it parked → *Resolution:* /maintain logs it as intentionally dormant, stops flagging it as a stale-snapshot gap, and won't re-queue unless it resurfaces.
**Your answer:** Parked. Deprioritised behind Mycelium, Growify and the Reality Architects/work merge. Marked dormant: true on the snapshot; no next_actions filed.
## Q3 — [decay.rotting_action] Growify self-folder/migration cluster — done, superseded, or still needed?
**Context:** Four actions from the 2026-06-29 session-2 brain dump are now 57d in backlog — `growify-dan-build-self-folders` (self-folder structure for Rishab + template for Disha), `growify-dan-migrate-workflowy-airtable` (migrate Rishab's Workflowy/Airtable exports into the folder structure), `growify-rishab-send-airtable`, and `growify-rishab-send-workflowy` (Rishab to send those exports). They've now been absent from Growify's current_focus/next_actions for three consecutive snapshot refreshes (last current as of 2026-07-30). The 2026-07-30 snapshot describes the Hermes build reading directly from "the real Growify context folder... migrated to a new private GitHub repo `growify-context`" — a different migration path than a Workflowy/Airtable export. Carried forward a third run.
**The call:** Did the self-folder build and export migration happen as part of the Hermes build (making these obsolete), did they quietly fall off the agenda, or are they still needed separately from the GitHub-repo migration that did happen?
**Options:**
- A) All four superseded by the actual GitHub-repo migration → *Resolution:* /maintain moves all four to `done/` with a dropped note (superseded by the growify-context repo migration).
- B) Self-folder build + migration (Dan's two) done, Rishab's two exports still outstanding → *Resolution:* /maintain moves `growify-dan-build-self-folders` and `growify-dan-migrate-workflowy-airtable` to `done/`, leaves the two Rishab-owned export items in backlog with a note confirming they're still live.
- C) All four still needed, just hasn't come up → *Resolution:* /maintain leaves all four in backlog with a note confirming they're still active, won't re-flag as rotting for 14 days.
**Your answer:** All four superseded by the growify-context repo migration. Moved to done/.
## Q4 — [decay.rotting_action] Growify session-1 leftovers — still live or drop?
**Context:** Three actions from the 2026-06-13 session-1 brain dump are now 73d in backlog — `growify-zoho-timeline` (confirm Zoho migration timeline with Rishab), `growify-brand-context-map` (map brand-level context fields), and `growify-team-context-fields` (define team-level context fields). None have appeared in Growify's current_focus, next_actions, or tensions across seven consecutive snapshot refreshes; the pilot's attention has moved to the narrower Rishab/Disha self-folder + Hermes work instead. Carried forward a fourth run.
**The call:** Are these three still active threads worth tracking, or have they quietly fallen off the agenda in favor of the narrower pilot scope?
**Options:**
- A) Still live, just hasn't come up → *Resolution:* /maintain leaves all three in backlog with a note that Dan confirmed they're still active, and won't re-flag them as rotting for 14 days.
- B) They've fallen off, drop them → *Resolution:* /maintain moves all three to `done/` with a dropped note (revisit if Rishab raises them again).
- C) Mixed — some live, some dropped → *Resolution:* free-text which is which; /maintain applies A to the ones you name live and B to the rest.
**Your answer:** Dropped. Fell off with the narrowed pilot scope. Moved to done/.
## Q5 — [decay.rotting_action] Growify image/ad workflow test — still live or superseded?
**Context:** Two linked actions from the 2026-06-05 brain dump are now 81d in backlog — `2026-06-05-growify-send-assets-and-brief` (Disha to send 5 raw images + resizing specs + ad brief) and `2026-06-05-growify-test-image-and-ad-workflows` (Dan to test image resizing/ad creative workflows on those assets). Neither appears in Growify's current_focus or next_actions, which have narrowed to the Phase 2 proposal + Hermes work; Disha in particular still hasn't replied since the 2026-07-11 self-folder session ask. Carried forward a fourth run.
**The call:** Is the original image/ad workflow test still something you want from Disha, or has it been superseded by the narrower pilot scope?
**Options:**
- A) Still want it, keep chasing → *Resolution:* /maintain leaves both in backlog, notes Dan confirmed relevance, won't re-flag as rotting for 14 days.
- B) Superseded, drop both → *Resolution:* /maintain moves both to `done/` with a dropped note (superseded by the narrower context-folder pilot).
**Your answer:** Dropped. Superseded by the narrower context-folder pilot. Moved to done/.
---

_All five answered and applied in-session 2026-08-25. Archived._
