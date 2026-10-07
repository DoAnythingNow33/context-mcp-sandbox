## 2026-09-27 — /maintain (headless, CI)
**Open items: 14** (going quiet 13 · loose ends 0 · mechanics 1)

### Applied from interview
Nothing. `_maintenance-interview.md` (generated 2026-09-20) was still fully blank — no `Your answer:` lines filled in. Per Step 0, archived to `_maintenance-interview-answered-27-09-26.md` and all three questions carried forward into a fresh interview with refreshed day counts. Checked for new evidence first — no commits touched `disha.md`, `growify.md`, `jamie-cameron.md`, or `self/goals.md` since 2026-09-20, so nothing changed underneath these questions.

### Auto-fixed
- `[cohere.index_drift]` — none flagged this run.
- `[cohere.unused_ip]` — 45 entries flagged `content_made: false`, 0 older than 30d — nothing to queue.
- Regenerated `_digest.md` (15 entities).

### Acted (judgment)
- **Unfiled next_actions check** (Step 3, "YOU OWN THIS CHECK NOW") — could not run. No Notion tool access in this CI session (`docs/SESSION-HANDOFF.md` Outstanding #1: still no `NOTION_TOKEN`). Skipped rather than guessed at Notion state — unchanged from the last four runs.
- **Rotting/stale actions check** (Step 3, "NOW A NOTION VIEW") — could not run, same reason.
- **13 quiet entities** (Disha, Sam/Explorers Club, Fadwa, Family, Growify, Jamie Cameron, Sebastian, Shereen, Victoria Russel, Mycelium, Sleevenote, DoAnythingNow, Token Sniper) — same set as last run, no new entity joined the list. Could not verify existing Notion coverage without Notion access, so not individually re-queued; folded into the Notion-access gap above. Tooling gap, not new decay.
- `entities/people/disha.md` (61d stale), `entities/people/growify.md` (59d stale), `entities/people/jamie-cameron.md` (59d stale) — all past the 21-day guard, unchanged since 2026-09-20. No new evidence to resolve Q1–Q3; carried forward with refreshed day counts only.

### Queued for interview
- Q1 [decay.rotting_action, Notion row] `outreach-review-emails-send-10` — now 96d overdue; still wanted, or superseded by `/prospect` + the Notion Prospects database?
- Q2 [decay.stale_doing, Notion row] `jamie-next-engagement` — closed by the joint venture, or still tracking a real open question (revenue/role split)?
- Q3 [acct.unfiled_next_action] Disha follow-up (self-folder + personal AI setup) — still worth one more chase, or let it go the way of the rest of the Growify self-folder cluster?

Net effect: nothing written to entities or Notion this run — vault-mechanical layer is clean (no drift, no new unused IP, digest current). Fifth consecutive run blocked on the same missing piece: Notion tool access in CI (`docs/SESSION-HANDOFF.md` Outstanding #1).

## 2026-09-20 — /maintain (headless, CI)
**Open items: 14** (going quiet 13 · loose ends 0 · mechanics 1)

### Applied from interview
Nothing. `_maintenance-interview.md` (generated 2026-09-13) is still fully blank — no `Your answer:` lines filled in. Per Step 0, not archived; all three questions carried forward with refreshed day counts.

Notable, though: `git log` shows Dan/Hermes briefly *did* act on the 2026-08-30 answers on 2026-09-17 (commit `9103f9c`) — closing `outreach-review-emails-send-10` and rewording `jamie-next-engagement` — but reverted it two minutes later (`30b6b93`). The edits targeted `actions/doing/` and `actions/done/`, which have been a frozen archive since the 2026-09-02 Notion migration; reverting was correct. The direction of those edits (close Q1, reword Q2) is a real signal of Dan's intent and is noted on the questions below, but the actual resolution still has to happen in Notion, not by editing vault action files.

### Auto-fixed
- `[cohere.index_drift]` — none flagged this run.
- `[cohere.unused_ip]` — 45 entries flagged `content_made: false`, 0 older than 30d — nothing to queue.
- Regenerated `_digest.md` (15 entities).

### Acted (judgment)
- **Unfiled next_actions check** (Step 3, "YOU OWN THIS CHECK NOW") — could not run. No Notion tool access in this CI session (`docs/SESSION-HANDOFF.md` Outstanding #1: no `NOTION_TOKEN`). Skipped rather than guessed at Notion state — unchanged from the last three runs.
- **Rotting/stale actions check** (Step 3, "NOW A NOTION VIEW") — could not run, same reason.
- **12 recurring quiet entities** (Disha, Sam/Explorers Club, Fadwa, Family, Growify, Jamie Cameron, Sebastian, Shereen, Victoria Russel, Mycelium, Sleevenote, DoAnythingNow) — could not verify existing Notion coverage without Notion access, so not individually re-queued; folded into the Notion-access gap above. Tooling gap, not new decay.
- **New: Token Sniper** (`[decay.quiet_entity]`, snapshot 20d old, no meetings logged) — reviewed against `entities/projects/token-sniper.md`: it's a solo automated Discord-bot project with no client relationship, so "no meetings" is structurally expected, not a decay signal (same call as Sleevenote's first appearance on 2026-07-26). No action, not queued.
- `entities/people/disha.md` (54d stale), `entities/people/growify.md` (52d stale), `entities/people/jamie-cameron.md` (52d stale) — all past the 21-day guard, unchanged since 2026-09-13. No new evidence to resolve Q1–Q3; carried forward with refreshed day counts and the interview-revert context above.

### Queued for interview
- Q1 [decay.rotting_action, now a Notion row] `outreach-review-emails-send-10` — now 89d overdue; still wanted, or superseded by `/prospect` + the Notion Prospects database? (Dan's 2026-09-17 edit-then-revert leans "close it," unconfirmed.)
- Q2 [decay.stale_doing, now a Notion row] `jamie-next-engagement` — closed by the joint venture, or still tracking a real open question (revenue/role split)? (Dan's 2026-09-17 edit-then-revert leans "reword, keep active," unconfirmed.)
- Q3 [acct.unfiled_next_action] Disha follow-up (self-folder + personal AI setup) — still worth one more chase, or let it go the way of the rest of the Growify self-folder cluster?

Net effect: nothing written to entities or Notion this run — vault-mechanical layer is clean (no drift, no new unused IP, digest current). Fourth consecutive run blocked on the same missing piece: Notion tool access in CI (`docs/SESSION-HANDOFF.md` Outstanding #1).

## 2026-09-13 — /maintain (headless, CI)
**Open items: 13** (going quiet 12 · loose ends 0 · mechanics 1)

### Applied from interview
Nothing. `_maintenance-interview.md` (generated 2026-09-06) was still fully blank — no `Your answer:` lines filled in. Per Step 0, archived to `_maintenance-interview-answered-13-09-26.md` and all three questions carried forward into a fresh interview with refreshed day counts (Q1 now 82d overdue vs. due date; Q2/Q3 snapshot staleness now 45–47d). Checked for new evidence on all three threads first — no commits touched `disha.md`, `growify.md`, `jamie-cameron.md`, or `self/goals.md`'s outreach line since the 2026-09-06 run, so nothing changed underneath these questions.

### Auto-fixed
- `[cohere.index_drift]` — none flagged this run.
- `[cohere.unused_ip]` — 45 entries flagged `content_made: false`, 0 older than 30d — nothing to queue.
- Regenerated `_digest.md` (15 entities).

### Acted (judgment)
- **Unfiled next_actions check** (Step 3, "YOU OWN THIS CHECK NOW") — could not run. No Notion tool access in this CI session (`docs/SESSION-HANDOFF.md` Outstanding #1: no `NOTION_TOKEN`). Skipped rather than guessed at Notion state — unchanged from the last two runs.
- **Rotting/stale actions check** (Step 3, "NOW A NOTION VIEW") — could not run, same reason.
- **12 quiet entities** (Disha, Sam/Explorers Club, Fadwa, Family, Growify, Jamie Cameron, Sebastian, Shereen, Victoria Russel, Mycelium, Sleevenote, DoAnythingNow) — could not verify existing Notion coverage without Notion access, so not individually re-queued; folded into the Notion-access gap above. Tooling gap, not new decay.
- `entities/people/disha.md` (47d stale), `entities/people/growify.md` (45d stale), `entities/people/jamie-cameron.md` (45d stale) — all past the 21-day guard, unchanged since 2026-08-30. No new evidence to resolve Q1–Q3; carried forward with refreshed day counts only.

### Queued for interview
- Q1 [decay.rotting_action, now a Notion row] `outreach-review-emails-send-10` — still wanted, or superseded by `/prospect` + the Notion Prospects database?
- Q2 [decay.stale_doing, now a Notion row] `jamie-next-engagement` — closed by the joint venture, or still tracking a real open question (revenue/role split)?
- Q3 [acct.unfiled_next_action] Disha follow-up (self-folder + personal AI setup) — still worth one more chase, or let it go the way of the rest of the Growify self-folder cluster?

Net effect: nothing written to entities or Notion this run — vault-mechanical layer is clean (no drift, no new unused IP, digest current). Third consecutive run blocked on the same missing piece: Notion tool access in CI (`docs/SESSION-HANDOFF.md` Outstanding #1).

## 2026-09-06 — /maintain (headless, CI)
**Open items: 13** (going quiet 12 · loose ends 0 · mechanics 1)

### Applied from interview
Nothing. The 2026-08-30 interview (`_maintenance-interview.md`) is still fully blank — no `Your answer:` lines filled in. Per Step 0, not archived. Its three questions targeted vault action files (`outreach-review-emails-send-10.md`, `jamie-next-engagement.md`, a Disha follow-up action) that no longer exist as vault files — all live actions migrated to the Notion Tasks Tracker on 2026-09-02 (confirmed: none of the three slugs appear anywhere in `actions/`, including the frozen `done/`/`cancelled/` archive, so they moved as still-open rows). Reworded to Notion-native resolutions and carried forward below rather than dropped — the underlying decisions are unchanged and still Dan's call.

### Auto-fixed
- `[cohere.index_drift]` — none flagged this run.
- `[cohere.unused_ip]` — 45 entries flagged `content_made: false`, 0 older than 30d — nothing to queue.
- Regenerated `_digest.md` (15 entities).

### Acted (judgment)
- **Unfiled next_actions check** (Step 3, "YOU OWN THIS CHECK NOW") — could not run. This check requires querying the Notion Tasks Tracker directly; this CI session has no Notion tool access (`docs/SESSION-HANDOFF.md` Outstanding #1: "CI has no `NOTION_TOKEN`"). Skipped rather than guessed at Notion state.
- **Rotting/stale actions check** (Step 3, "NOW A NOTION VIEW") — could not run, same reason: would need the Tasks Tracker Active view sorted by last-edited.
- **12 quiet entities** (Disha, Sam/Explorers Club, Fadwa, Family, Growify, Jamie Cameron, Sebastian, Shereen, Victoria Russel, Mycelium, Sleevenote, DoAnythingNow) — could not verify existing Notion coverage without Notion access, so not individually re-queued as 12 new findings; folded into the single Notion-access gap noted above. This is a tooling gap, not new decay — no different from last run's state.
- `entities/people/disha.md` (40d stale), `entities/people/growify.md` (38d stale), `entities/people/jamie-cameron.md` (38d stale) — all past the 21-day guard, unchanged since 2026-08-30 (no meetings, no edits). No new evidence to resolve Q1–Q3 below; carried forward as-is.

### Queued for interview
- Q1 [decay.rotting_action, now a Notion row] `outreach-review-emails-send-10` — still wanted, or superseded by `/prospect` + the Notion Prospects database?
- Q2 [decay.stale_doing, now a Notion row] `jamie-next-engagement` — closed by the joint venture, or still tracking a real open question (revenue/role split)?
- Q3 [acct.unfiled_next_action] Disha follow-up (self-folder + personal AI setup) — still worth one more chase, or let it go the way of the rest of the Growify self-folder cluster?

Net effect: nothing written to entities, actions, or Notion this run — the vault-mechanical layer is clean (no drift, no new unused IP, digest current), and every substantive open question is blocked on the same missing piece: Notion tool access in CI. That's an infrastructure gap already tracked (`docs/SESSION-HANDOFF.md` Outstanding #1), not a new backlog item.

## 2026-08-30 — /maintain (headless, CI)
**Open items: 25** (going quiet 22 · loose ends 2 · mechanics 1)

### Applied from interview
Nothing — no unresolved interview was outstanding (the 2026-08-25 interview was fully answered and archived in-session).

### Auto-fixed
- No index drift, no misfiled actions, no unused-IP entries past 30d this run.
- `entities/people/santiago-bonita.md` — added `dormant: true` (matches the new dormant-entity mechanism introduced 2026-08-25; the snapshot already described it as archived with no next steps queued, so `system_health.py` now skips it instead of re-flagging it as quiet every week).
- Regenerated `_digest.md`.

### Acted (judgment)
- **13 quiet entities** (Disha, Sam/Explorers Club, Fadwa, Family, Growify, Jamie Cameron, Sebastian, Shereen, Victoria, Mycelium, Sleevenote, DoAnythingNow, Santiago/Bonita) — every one already has a live open action covering it except Santiago, which is now formally dormant (see above). Logged covered, nothing filed.
- `actions/backlog/2026-06-26-three-initiatives-next-steps.md` — moved to `done/`, superseded: all three sub-threads (Sleevenote pitch deck, carousel templates, website identity) were already broken out into their own tracked actions back in July.
- `actions/backlog/explorers-club-sam-notion-setup.md`, `get-3-more-skilljar-certificates.md`, `growify-phase-2-proposal.md`, `shereen-confirm-scope.md`, `2026-07-13-carousel-templates-system.md`, `2026-07-13-sleevenote-pitch-deck-prep.md`, `2026-07-13-website-identity-distillation.md` — all still genuinely relevant per current context (self/goals.md, entities/people/shereen.md); annotated with this week's rotting note, left in place.
- `actions/doing/jamie-next-engagement.md` — annotated stale-in-doing (66d).

### Queued for interview
- Whether `outreach-review-emails-send-10.md` (68d, due 2026-06-23) is still wanted as-is or superseded by the Notion prospecting workflow (`/prospect`, migrated 2026-08-14).
- Whether `jamie-next-engagement.md` (doing, 66d) should close — the underlying question looks answered by the joint pitch-deck venture — or stay open for something more specific.
- Disha follow-up (self-folder + personal AI setup) — both `entities/people/disha.md` (33d stale) and `entities/people/growify.md` (31d stale) name it as an unfiled next_action, but both snapshots are past the 21-day staleness guard, so nothing was filed from them this run.

**Open items: 22** (going quiet 19 · loose ends 2 · mechanics 1) · backlog 55 · doing 1 · done 37

All five outstanding questions answered directly with Dan and applied on the
spot rather than deferred to the next scheduled run. First interview cleared
since 2026-07-26 — the previous eight runs went unanswered because the Discord
upload was failing with a 400 and the file never reached him (fixed 2026-08-25).

### Applied
- **Q1 Soho Spirits Festival** — festival happened; Dan wants the outcome, not the prep. Dropped `dan-intro-victoria-nothing-headphones`, `victoria-dm-tom-sleevenote-festival`, `victoria-email-anthony-vinyl-factory-visit`, `victoria-text-tony-calabasa-booth` to `done/` as time-expired. Filed `victoria-catchup-festival-outcome` to cover the booth result, the Phonica and Tom/Sleevenote threads, whether Sleevenote is in or out, and a refresh of Victoria's snapshot (still dated 2026-08-11, pre-festival).
- **Q2 Ontology for Creatives** — parked. Snapshot marked `dormant: true` with reason and date. `system_health.py` now skips dormant entities entirely, so it stops being flagged as quiet or stale; its two next_actions were deliberately not filed.
- **Q3 Growify self-folder cluster** — all four superseded by the `growify-context` private repo migration that actually happened; the Workflowy/Airtable export path was never taken. Moved to `done/`.
- **Q4 Growify session-1 leftovers** — dropped. Absent from seven consecutive snapshots after the pilot narrowed to Rishab/Disha. Moved to `done/`.
- **Q5 Growify image/ad workflow test** — dropped. Superseded by the narrower pilot; Disha unresponsive since 2026-07-11. Moved to `done/`.

### Net effect
13 actions closed, 1 filed, 1 entity parked. Backlog 67 → 55. Every remaining
rotting item is now something genuinely still live rather than a decision Dan
had already made and never recorded.

### Also this session
The health score was retired at Dan's call — see the commit "Retire the health
score; fix action dating in CI". `dormant: true` on an entity snapshot is a new
mechanism introduced here for parking a thread without it reading as decay.

# Maintenance Log — Q3 2026

## 2026-08-25 — /maintain
**Health: 11/100** (was 11)

### Applied from interview
Nothing. The 2026-08-23 interview is still fully blank (no `Your answer:` lines filled in) — per Step 0, skipped straight to Step 1 rather than archiving it. All seven of its questions are carried forward below with refreshed numbers.

### Auto-fixed
- Misfiled actions: scanned all three `actions/` folders — one non-match found (`2026-06-26-three-initiatives-next-steps.md`, still has no `status` field at all, not a real action-item file, out of scope, left untouched)
- `[cohere.index_drift]` — none flagged this run
- `[cohere.unused_ip]` — 45 entries flagged `content_made: false`, 0 older than 30d — nothing to queue
- Regenerated `_digest.md` (14 entities)

### Acted (judgment)
- `[acct.unfiled_next_action]` Fadwa — snapshot refreshed since last run (now 12d old, current again) and its `current_state` already shows the answer to carried Q2: final session happened 2026-07-31, engagement was re-scoped (not closed) into paid context-folder sessions. Moved `fadwa-confirm-session.md` → `done/` (superseded by the re-scope) and filed the two still-open next_actions (`fadwa-confirm-pricing.md`, `fadwa-log-rescope-meeting.md`). **Q2 dropped from the interview — resolved by newer snapshot data, no longer needs Dan's call.**
- `[acct.unfiled_next_action]` Victoria Russel — snapshot current (14d old); filed `victoria-connect-dean-case-project.md`, no existing loose match
- `[acct.unfiled_next_action]` Ontology for Creatives × 2 — snapshot now 27d stale (past the 21d guard), next_actions not filed, folded into carried Q3 (still unresolved)
- `[decay.quiet_entity]` × 8 — Disha, Sam/Explorers Club, Family, Growify, Sebastian, Shereen, Sleevenote already covered by existing open actions; Santiago/Bonita explicitly archived per Dan's 2026-07-13 call, no chase
- `[decay.quiet_entity]` Jamie Cameron — no open action existed; filed `check-in-jamie-cameron.md` as a general check-in rather than pulling from the snapshot's next_actions (now 26d stale, past the guard)
- `[decay.quiet_entity]` Ontology for Creatives — no open action, but folded into carried Q3 (stale-snapshot call) rather than filing a blind check-in
- `[decay.rotting_action]` × 3 (`2026-07-13-carousel-templates-system`, `2026-07-13-sleevenote-pitch-deck-prep`, `2026-07-13-website-identity-distillation`) confirmed against unchanged `self/goals.md` — still relevant / deferred as intended, annotated in place. Sleevenote note now also carries the "cooling as of 2026-08-11" context from goals.md.
- `[decay.rotting_action]` `jamie-notion-ai-assistant-mvp-spec` (36d) confirmed against Jamie's 2026-07-30 snapshot — still relevant, annotated in place
- `[decay.rotting_action]` × 2 (`dan-propose-victoria-sync-cadence`, `victoria-confirm-sync-cadence`, 14d each) and `victoria-review-littleguy-net` (14d) — first time crossing the 10d threshold; confirmed against Victoria's current 2026-08-11 snapshot next_actions — still relevant, annotated in place
- `[decay.rotting_action]` `dan-build-notion-workspace-victoria-partnership` (18d) and `dan-intro-leighton-sleevenote-gtm` (14d) — confirmed against Victoria's current snapshot — still relevant, annotated in place
- `[decay.rotting_action]` × 4 festival-dated items (`dan-intro-victoria-nothing-headphones`, `victoria-dm-tom-sleevenote-festival`, `victoria-email-anthony-vinyl-factory-visit`, `victoria-text-tony-calabasa-booth`, 18d each) — the Soho Spirits Festival (21-22 Aug) has now passed and Victoria's snapshot (last updated 2026-08-11, pre-festival) was never refreshed with the outcome. Not confidently resolvable either way — annotated in place, new interview question queued (Q8)
- `[decay.rotting_action]` × 4 Growify self-folder/migration cluster (57d) — still unresolved, carried forward again (Q5)
- `[decay.rotting_action]` × 3 Growify session-1 leftovers (73d) — still unresolved, carried forward again (Q6)
- `[decay.rotting_action]` × 2 Growify image/ad workflow (81d) — still unresolved, carried forward again (Q7)
- `[acct.ratio]` 0.46 (50 created / 23 done), 8th consecutive run below the 0.5 floor — re-queued with standing sprint-capacity context (Q4)
- `[cohere.orphan_meeting]` `meetings/context.md` — false positive again, this is the meetings/ workspace README, not a meeting record; skipped, not queued
- `[decay.dpl_gap]` 14 of 14 days unlogged (window has rolled forward, still full) — re-queued as top-priority interview item (Q1), still the single biggest lever on the score

### Queued for interview
- Q1 [decay.dpl_gap] — 14 days unlogged (2026-08-12 → 2026-08-25), backfill / accept / rethink cadence
- Q2 — dropped, resolved by Fadwa's refreshed snapshot (see above)
- Q3 [acct.unfiled_next_action] — Ontology for Creatives snapshot now 27d stale — refresh or park?
- Q4 [acct.ratio] — 0.46, 8th consecutive run below floor — block time or accept as new normal?
- Q5 [decay.rotting_action] — Growify self-folder/migration cluster (4 actions, 57d) — done, mixed, or still needed?
- Q6 [decay.rotting_action] — Growify session-1 leftovers (3 actions, 73d) — still live or drop?
- Q7 [decay.rotting_action] — Growify image/ad workflow test (2 actions, 81d) — still live or superseded?
- Q8 [decay.rotting_action] — NEW: Soho Spirits Festival (21-22 Aug, now past) — did it happen, and are the 4 prep actions moot?

## 2026-08-23 — /maintain
**Health: 17/100** (was 17)

### Applied from interview
Nothing. The 2026-08-16 interview was still fully blank (no `Your answer:` lines filled in) — per Step 0, skipped straight to Step 1 rather than archiving it. All five of its questions are carried forward below with refreshed numbers.

### Auto-fixed
- Misfiled actions: scanned all three `actions/` folders — none found (`2026-06-26-three-initiatives-next-steps.md` still has no `status` field, out of scope, left untouched)
- `[cohere.index_drift]` — none flagged this run
- `[cohere.unused_ip]` — 43 entries flagged `content_made: false`, 0 older than 30d — nothing to queue
- Regenerated `_digest.md` (14 entities)

### Acted (judgment)
- `[decay.quiet_entity]` × 14 — Disha, Sam/Explorers Club, Fadwa, Family, Growify, Jamie Cameron, Sebastian, Shereen, Victoria Russel, Sleevenote, DoAnythingNow, Mycelium already covered by existing open actions; Santiago/Bonita explicitly archived per Dan's 2026-07-13 call, no chase; Ontology for Creatives has no open action but is 25d stale — folded into the new stale-snapshot interview question (Q3) instead of filing a blind check-in
- `[acct.unfiled_next_action]` Fadwa (snapshot 26d stale, past the 21d guard) — next_action not filed, folded into carried Q2 (final-session/closure call)
- `[acct.unfiled_next_action]` Ontology for Creatives × 2 (snapshot 25d stale, just past the 21d guard) — next_actions not filed, new interview question queued (Q3)
- `[decay.rotting_action]` `jamie-email-meeting-summary-action-items` (34d) → moved to `done/` — superseded: the joint pitch deck is already built and live (jamie-pitch.vercel.app), and the individual 07-20 action items are already tracked in their own actions (MVP spec, deck-link feedback)
- `[decay.rotting_action]` × 3 (`2026-07-13-carousel-templates-system`, `2026-07-13-sleevenote-pitch-deck-prep`, `2026-07-13-website-identity-distillation`) confirmed against unchanged `self/goals.md` — still relevant / deferred as intended, annotated in place
- `[decay.rotting_action]` `jamie-notion-ai-assistant-mvp-spec` (34d) confirmed against Jamie's 2026-07-30 snapshot next_actions — still relevant, annotated in place
- `[decay.rotting_action]` × 4 Growify self-folder/migration cluster (55d) — still unresolved, carried forward again (Q5)
- `[decay.rotting_action]` × 3 Growify session-1 leftovers (71d) — still unresolved, carried forward again (Q6)
- `[decay.rotting_action]` × 2 Growify image/ad workflow (79d) — still unresolved, carried forward again (Q7)
- `[acct.ratio]` 0.44 (50 created / 22 done), 7th consecutive run below the 0.5 floor — re-queued with standing sprint-capacity context (Q4)
- `[cohere.orphan_meeting]` `meetings/context.md` — false positive again, this is the meetings/ workspace README, not a meeting record; skipped, not queued
- `[decay.dpl_gap]` 14 of 14 days unlogged — queued as top-priority interview item (Q1), the single biggest lever on the 17/100 score

### Queued for interview
- Q1 [decay.dpl_gap] — 14 days unlogged (2026-08-10 → 2026-08-23), backfill / accept / rethink cadence
- Q2 [acct.unfiled_next_action] — Fadwa final session (2026-07-31) — happened, slipped, or closed?
- Q3 [acct.unfiled_next_action] — Ontology for Creatives snapshot 25d stale — refresh or park?
- Q4 [acct.ratio] — 0.44, 7th consecutive run below floor — block time or accept as new normal?
- Q5 [decay.rotting_action] — Growify self-folder/migration cluster (4 actions, 55d) — done, mixed, or still needed?
- Q6 [decay.rotting_action] — Growify session-1 leftovers (3 actions, 71d) — still live or drop?
- Q7 [decay.rotting_action] — Growify image/ad workflow test (2 actions, 79d) — still live or superseded?

## 2026-08-16 — /maintain
**Health: 13/100** (was 13)

### Applied from interview
- Q1 [decay.dpl_gap] — Dan answered (free text): the DPL gap is structural, not a discipline lapse — left Farmer J 2026-07-10, now driving delivery for Ottolenghi's CPU (Sat–Mon 6am–1pm) with baby #2 due end of August and a 2-year-old at home; the day is now family-first with business happening in opportunistic sprints. Applied as: accepted, not chased — logged as resolved context rather than requeued as a gap-count question. Dan's ask to rethink `/dpl`'s daily-cadence assumption is a skill-design change outside `/maintain`'s mechanical scope — flagged here for follow-up, not auto-implemented.
- Q2–Q5 (ratio, Fadwa, Growify session-1 leftovers, Growify image/ad workflow) — left blank, carried forward into today's interview with refreshed numbers.

### Auto-fixed
- Misfiled actions: scanned all three `actions/` folders — none found, all frontmatter matches folder placement (`2026-06-26-three-initiatives-next-steps.md` still has no `status` field, out of scope, left untouched)
- `[cohere.index_drift]` — none flagged this run
- `[cohere.unused_ip]` — 43 entries flagged `content_made: false`, 0 older than 30d — nothing to queue
- Regenerated `_digest.md` (13 entities)

### Acted (judgment)
- `[decay.quiet_entity]` × 13 — all covered without new chase actions: Disha, Sam/Explorers Club, Fadwa, Family, Growify, Jamie Cameron, Sebastian, Shereen, Victoria Russel, Sleevenote, DoAnythingNow already have open backlog actions tracking them; Santiago/Bonita is explicitly archived per Dan's own 2026-07-13 call (no chase); Mycelium had no open action, now covered by the three newly-filed next_actions below
- `[acct.unfiled_next_action]` Mycelium (snapshot current, 18d) — filed three backlog actions: `mycelium-add-concept-detail.md`, `mycelium-define-legal-structure-options.md`, `mycelium-identify-first-people.md`
- `[acct.unfiled_next_action]` Growify (snapshot current, 17d; no existing loose match) — filed `growify-monitor-openrouter-balance.md`
- `[acct.unfiled_next_action]` Jamie Cameron (snapshot current, 17d; no existing loose match) — filed `jamie-send-deck-link-feedback.md`
- `[acct.unfiled_next_action]` Fadwa — "Hold the final session" is past-dated and already the unresolved Q1 below; not filed
- `[decay.rotting_action]` `growify-dan-hermes-setup.md` (48d) → moved to `done/` — the file's own notes already describe the build as shipped and tested end-to-end (2026-07-29) plus a completed follow-up (2026-07-30); no longer appears in Growify's current 2026-07-30 snapshot
- `[decay.rotting_action]` `jamie-pitch-deck-smb-enterprise-ai.md` (27d) → moved to `done/` — Jamie's 2026-07-30 snapshot confirms the deck is built and live at jamie-pitch.vercel.app; follow-up now tracked separately (`jamie-send-deck-link-feedback.md`)
- `[decay.rotting_action]` × 3 (`2026-07-13-carousel-templates-system`, `2026-07-13-sleevenote-pitch-deck-prep`, `2026-07-13-website-identity-distillation`) confirmed against unchanged `self/goals.md` 2026-07-28, and × 2 Jamie items (`jamie-email-meeting-summary-action-items`, `jamie-notion-ai-assistant-mvp-spec`) confirmed against Jamie's 2026-07-30 snapshot — still relevant, annotated in place, left in backlog
- `[decay.rotting_action]` × 4 Growify self-folder/migration cluster (`growify-dan-build-self-folders`, `growify-dan-migrate-workflowy-airtable`, `growify-rishab-send-airtable`, `growify-rishab-send-workflowy`, 48d) — dropped out of Growify's current_focus/next_actions for the first time this run after 5 straight "still relevant" confirmations; genuinely ambiguous whether they were folded into the Hermes build's actual migration (a different GitHub-repo path) or just fell off the agenda — queued rather than guessed (Q3, new)
- `[decay.rotting_action]` × 3 Growify session-1 leftovers and × 2 Growify image/ad workflow items — still unresolved carry-forwards, re-queued with fresh day counts (Q4, Q5)
- `[acct.ratio]` 0.44 (45 created / 20 done), 6th consecutive run below the 0.5 floor — re-queued with the sprint-based-capacity context from Q1 attached (Q2)
- `[cohere.orphan_meeting]` `meetings/context.md` — false positive again, this is the meetings/ workspace README, not a meeting record; skipped, not queued

### Queued for interview
- Q1 — [acct.unfiled_next_action] Fadwa — did the 2026-07-31 final session happen, is the engagement closed out? (carried forward, 2nd run)
- Q2 — [acct.ratio] 0.44, 6th straight run below the 0.5 floor, now with sprint-based-capacity context attached
- Q3 — [decay.rotting_action] Growify self-folder/migration cluster (4 items, 48d) — done via the Hermes build, superseded, or still needed? (new)
- Q4 — [decay.rotting_action] Growify session-1 leftovers (3 items, 64d) — still live or dropped? (carried forward, 2nd run)
- Q5 — [decay.rotting_action] Growify image/ad workflow test (2 items, 72d) — still live or superseded? (carried forward, 2nd run)

Score sits at 13/100, unchanged from the nightly reading — the DPL gap (now 14/14 days, unbroken since 2026-07-27) and the sub-floor commit→done ratio are still the two biggest drags, and both carried zero response through last week's interview. What did move: two long-rotting actions turned out to be genuinely done (Growify's Hermes pipeline, Jamie's pitch deck) and are now closed out instead of rotting further; five quiet entities and Mycelium's three unfiled next_actions are now covered by concrete open actions instead of implicit next_actions no one was tracking; and Dan's answer to last week's DPL question closed that specific gap-chasing loop for good — the vault now knows *why* the days are unlogged (a structural schedule change, not neglect) rather than re-asking the same question. The interview holds at 5 questions, but the shape shifted: Fadwa's closure and the ratio are the ones costing the most to leave sitting, since one is a real client relationship in limbo and the other has now gone unanswered for six straight weeks.

## 2026-08-09 — /maintain
**Health: 48/100** (was 48)

### Applied from interview
`_maintenance-interview.md` (generated 2026-08-02) was fully blank — no answers to apply. Per Step 0, it was not archived; its 4 questions carried forward into today's interview (Q1–Q4 below), refreshed with current data. Not archived, since nothing was answered.

### Auto-fixed
- Misfiled actions: scanned all three `actions/` folders for status/folder mismatches — none found (`2026-06-26-three-initiatives-next-steps.md` has no `status` field at all, so it isn't a reconcilable mismatch; left untouched, out of scope for this check)
- `[cohere.index_drift]` — no drift flagged this run, nothing to fix
- `[cohere.unused_ip]` — 43 entries flagged `content_made: false`, 0 older than 30d — nothing to queue
- Regenerated `_digest.md` (11 entities)

### Acted (judgment)
- `[decay.quiet_entity] Family` — covered: `check-in-family.md` and `family-finance-tracker-notion.md` already open in backlog
- `[decay.quiet_entity] Jamie Cameron` — covered: `jamie-catchup-and-social-trait-chase.md`, `jamie-catchup-week-0714.md`, `jamie-chase-social-trait-2.md` already open in backlog
- `[decay.quiet_entity] Santiago / Bonita` — no action: snapshot already marks this archived/dormant per Dan's 2026-07-13 call, next_actions intentionally empty
- `[acct.unfiled_next_action] Fadwa` — "Check in on how Circa Arts is landing" already covered by `fadwa-checkin-circa-arts.md`; "Hold the final session — 2026-07-31" is the unresolved Q3 below (session date has passed with no update)
- `[cohere.orphan_meeting] context` — false positive again: `meetings/context.md` is the workspace README, not a meeting record. Skipped.
- 11 `[decay.rotting_action]` items confirmed still relevant against current source (Growify's 2026-07-28 snapshot for the 5 pilot items; self/goals.md for the 3 carousel/sleevenote/website items; Jamie's 2026-07-20 snapshot for the 3 Jamie items) — annotated in place, left in backlog: `2026-07-13-carousel-templates-system.md`, `2026-07-13-sleevenote-pitch-deck-prep.md`, `2026-07-13-website-identity-distillation.md`, `growify-dan-build-self-folders.md`, `growify-dan-hermes-setup.md`, `growify-dan-migrate-workflowy-airtable.md`, `growify-rishab-send-airtable.md`, `growify-rishab-send-workflowy.md`, `jamie-email-meeting-summary-action-items.md`, `jamie-notion-ai-assistant-mvp-spec.md`, `jamie-pitch-deck-smb-enterprise-ai.md`
- 5 `[decay.rotting_action]` items are genuinely ambiguous (absent from current next_actions/current_focus across multiple runs, scope may have narrowed past them) — queued rather than guessed on: `growify-zoho-timeline`, `growify-brand-context-map`, `growify-team-context-fields` (Q4), `2026-06-05-growify-send-assets-and-brief`, `2026-06-05-growify-test-image-and-ad-workflows` (Q5)
- `[decay.dpl_gap]` and `[acct.ratio]` — both unresolved carry-forwards from the last two runs, re-queued with fresh numbers (Q1, Q2)

### Queued for interview
- Q1 — [decay.dpl_gap] 14/14 days missing, 2026-07-27 to 2026-08-09 — 5th straight fully-rolled gap, still the single biggest lever on the score
- Q2 — [acct.ratio] 0.45 (44 created / 20 done), 5th straight run below the 0.5 floor
- Q3 — [acct.unfiled_next_action] Fadwa — did the 2026-07-31 final session happen, is the engagement closed out?
- Q4 — [decay.rotting_action] Growify session-1 leftovers (zoho-timeline, brand-context-map, team-context-fields), 57d, absent from 4 consecutive snapshot refreshes — still live or dropped?
- Q5 — [decay.rotting_action] Growify image/ad workflow test (send-assets-and-brief, test-image-and-ad-workflows), 65d, superseded by the narrower self-folder pilot?

## 2026-07-13 — /maintain
**Health: 18/100** (was 28)

### Applied from interview
Resolved all 8 questions from `_maintenance-interview-answered-13-07-26.md`, archived.

- Q1 (DPL gap, 10 days) — Answer B: let them go. Added the 10 dates (2026-06-24, -25, -27, -28, -29, 2026-07-01 through -05) to `scripts/.health-suppress.json` under `dpl_gap_dates`, merged with the existing 9. Noted as accepted, not chased further.
- Q2 (content engine identity sentence) — Answer A: "DoAnythingNow helps humans remember the magic of being human again — creativity as the superpower in every part of life." Written into `self/identity.md` (new Mission section) and `self/goals.md` (Content engine bullet updated from "stalled" to "unblocked 2026-07-13"). Read `actions/backlog/2026-06-26-three-initiatives-next-steps.md` and filed the concrete gated items as three new backlog actions: `2026-07-13-sleevenote-pitch-deck-prep.md`, `2026-07-13-website-identity-distillation.md` (flagged low-priority — website is explicitly deferred per goals.md), `2026-07-13-carousel-templates-system.md`.
- Q3 (Disha second session) — Answer A: not yet held, scheduling for 2026-07-14. Bumped `entities/people/disha.md` `last_updated` → 2026-07-13, current_state and next_actions updated with the explicit 2026-07-14 date.
- Q4 (Family stale snapshot) — Answer B + new info: bumped `entities/people/family.md` `last_updated` → 2026-07-13, cleared the 3 resolved next_actions, added an External Reference section pointing to `/Users/DoAnythingNow./Desktop/TejadaScottFamily` (path only, not read).
- Q5 (Santiago/Bonita) — Answer B: stalled/dead. `entities/people/santiago-bonita.md` current_state rewritten to archived/inactive, tension added, next_actions cleared, `last_updated` → 2026-07-13. `self/goals.md` Business Threads line updated from "equity formalised" to "archived 2026-07-13, gone quiet."
- Q6 (Fadwa overdue items) — Answer B + new info: `actions/backlog/send-fadwa-white-paper.md` moved to `actions/done/` with a sent note. `entities/people/fadwa.md` updated — final payment received, final session upcoming (no date yet), `last_updated` → 2026-07-13. `fadwa-send-june-session-dates.md` reframed as "final session" rather than "June session," left open.
- Q7 (Shereen) — Answer A: still waiting, Dan calling her 2026-07-14. `entities/people/shereen.md` `last_updated` → 2026-07-13, next_actions updated to "Call Shereen 2026-07-14 to confirm scope/status."
- Q8 (orphan meeting date typo) — Answer A: confirmed typo. `git mv meetings/2025-06-05-growify-ontology.md → meetings/2026-06-05-growify-ontology.md`, `date:` frontmatter and body date corrected to 2026-06-05, linked from `entities/people/growify.md` and `calendar/2026/Q2/june-2026.md` Meetings sections.

### Auto-fixed
- `[cohere.index_drift]` — `index.md` dates corrected for Family, Disha Bhatnagar, Santiago/Bonita, Fadwa, Shereen (all → 2026-07-13)
- Misfiled actions: `actions/backlog/create-workshop-visuals.md` and `actions/backlog/update-skool-visuals.md` had `status: pending` (invalid value) while sitting correctly in `backlog/` — corrected frontmatter to `status: backlog`
- `[cohere.unused_ip]` — 30 IP entries >30d old with `content_made: false` appended to `ops/content/_idea-queue.md` (13 were already queued from 2026-06-22)
- Regenerated `_digest.md` (11 entities) — run twice, once after Step 2 auto-fixes and once after Step 3 judgment edits

### Acted (judgment)
- `fadwa-setup-monthly-billing.md` moved to `actions/done/` and marked dropped — the £80/month cadence no longer applies now Fadwa's engagement is closing (Q6 context)
- `growify-second-sessions-rishab-disha.md` — annotated with Disha's confirmed 2026-07-14 date; Rishab's second session still open
- Filed unfiled next_actions as new backlog items where genuinely not covered elsewhere: `jamie-catchup-and-social-trait-chase.md`, `victoria-log-meeting-and-clarify-scope.md`, `dan-integrate-logo-into-website.md`, `family-finance-tracker-notion.md`, `sleevenote-3d-clip-design-and-manufacturing.md`
- `[cohere.orphan_meeting] context` — confirmed false positive again: `meetings/context.md` is the workspace README, not a meeting file. Skipped.
- `[decay.quiet_entity] Sleevenote` (17d, no meetings) — reviewed: expected for a brand-new opportunity with no scheduled calls yet, not a real decay signal. No action.
- `[decay.stale_doing] jamie-next-engagement` (20d in doing) — reviewed against current (2026-07-11) Jamie snapshot: still genuinely in progress pending the 2026-07-14 catch-up. No action.
- `[acct.ratio]` 0.22 (9 created / 2 done) — reviewed: this session filed ~10 new backlog actions in one pass while only closing 2, which mechanically depresses the ratio. Not a real accountability problem; expected to self-correct as the newly filed items get worked. No suppression added — leaving it visible.
- Remaining `[decay.rotting_action]` findings on Growify/outreach/Explorers Club/Skilljar items — spot-checked against current entity snapshots; all still genuinely open and blocked on external parties (Rishab, Fadwa, Sam) or Dan's own bandwidth, consistent with prior runs' annotations. Not re-touched individually this pass to avoid cosmetic noise on unchanged items.

### Queued for interview
See fresh `_maintenance-interview.md` — 1 question.

## 2026-07-02 — /maintain
**Health: 43/100** (was 43)

### Applied from interview
Nothing — no open interview to resume (last one archived 2026-06-22).

### Auto-fixed
- `index.md` — corrected Sam / Explorers Club date column 2026-06-23 → 2026-06-24 to match snapshot `last_updated`
- Scaffolded `calendar/2026/Q3/` (didn't exist yet — today is the first day of the quarter)
- Regenerated `_digest.md` (9 entities)
- Scanned `actions/{backlog,doing,done}/` for status/folder mismatches — none found

### Acted (judgment)
- Explorers Club (snapshot current, 8d): filed 2 of 3 unfiled next_actions as new backlog actions (`explorers-club-confirm-hike-brief-values.md`, `explorers-club-close-date-payment.md`); "send finished workspace" already covered by existing `explorers-club-sam-notion-setup.md`
- Growify (snapshot current, 9d): filed 1 of 5 unfiled next_actions (`growify-second-sessions-rishab-disha.md`); the other 4 already covered by existing backlog/done actions
- Jamie Cameron (snapshot current, 17d): both next_actions already covered by existing doing/done actions — nothing filed
- Sleevenote (snapshot current, 6d): all 5 next_actions already covered by `actions/backlog/2026-06-26-three-initiatives-next-steps.md` — nothing filed
- DoAnythingNow (snapshot current, 10d): filed 1 of 3 unfiled next_actions (`outreach-25-ai-workflows-approaches.md`); the other 2 already covered
- Fadwa (37d stale), Family (80d stale), Santiago/Bonita (66d stale), Shereen (39d stale): snapshots too old to trust — none of their next_actions filed, refresh queued for each
- Family: no open action existed for this quiet entity → filed `check-in-family.md`
- Fadwa, Jamie Cameron, Shereen: quiet-entity check covered by existing open actions — logged, nothing filed
- Santiago/Bonita: quiet entity with no open action and genuine dead-vs-quiet ambiguity → queued, not filed
- Rotting actions — 4 Growify session-1 items (`growify-brand-context-map`, `growify-posthog-review`, `growify-team-context-fields`, `growify-zoho-timeline`, 19d) and 3 Growify brain-dump items (`2026-06-05-growify-book-chandika-rohit-sessions`, `2026-06-05-growify-send-assets-and-brief`, `2026-06-05-growify-test-image-and-ad-workflows`, 27d): still relevant against the current Growify snapshot — re-stamped, left in place
- Rotting action `2026-06-05-growify-research-posthog` (27d): obsolete — superseded by `growify-posthog-share.md` (done) and `growify-posthog-review.md` (Rishab's decision now pending) → moved to `actions/done/`
- Rotting actions `fadwa-send-june-session-dates` and `send-fadwa-white-paper` (37d each, both now past their end-of-June due dates): unclear whether still live → left in place, queued
- Parked thread "Content engine — stalled" (`self/goals.md`): real strategic choice pending (the identity-sentence decision named in `actions/backlog/2026-06-26-three-initiatives-next-steps.md`) → left in place, queued
- `[cohere.orphan_meeting]` "context": false positive — `meetings/context.md` is the workspace context file, not a meeting — skipped, not queued
- `[cohere.orphan_meeting]` `2025-06-05-growify-ontology`: entity (Growify) is unambiguous but the date looks like a possible typo (predates the vault and the Growify engagement) → queued rather than guessing
- `[cohere.unused_ip]` 37 entries flagged, 0 older than 30d → nothing queued this run

### Queued for interview
- DPL gap — 7 of last 14 days unlogged, biggest lever on the health score
- Content engine — identity-sentence decision blocking restart
- Family — refresh 80d-stale snapshot
- Santiago/Bonita — alive or dead, plus 66d-stale snapshot refresh
- Fadwa — chase overdue June session dates + white paper, plus 37d-stale snapshot
- Shereen — refresh 39d-stale snapshot
- Orphan meeting `2025-06-05-growify-ontology` — confirm date before linking

## 2026-07-02 — /maintain (rerun)
**Health: 44/100** (was 43)

### Applied from interview
Nothing — the open interview from earlier today had no filled-in answers. Archived to `_maintenance-interview-answered-02-07-26.md`; all 7 questions carried forward into a fresh interview (two enriched with new evidence, see below).

### Auto-fixed
- Regenerated `_digest.md` (10 entities)
- Scanned `actions/{backlog,doing,done}/` for status/folder mismatches — none found (the one apparent hit, `2026-06-26-three-initiatives-next-steps.md`, isn't a kanban action file — no `status` field by design, it's a planning doc)
- `[cohere.unused_ip]` 41 entries flagged, 0 older than 30d → nothing queued

### Acted (judgment)
- Disha Bhatnagar (snapshot 27d stale, over the 21d guard threshold): next_actions not filed. Quiet-entity check: not queued — she's away and the snapshot itself notes she returns 2026-07-05, with `growify-second-sessions-rishab-disha.md` already covering the next step. Refresh isn't actionable until she's back, so not queued as a question.
- Growify: "Book Disha session" already covered by `growify-second-sessions-rishab-disha.md` (filed earlier today) — logged, nothing filed.
- Jamie Cameron (snapshot current, 17d): both next_actions already covered by existing `jamie-chase-social-trait.md` (done) and `jamie-next-engagement.md` (doing) — nothing filed. Quiet-entity check covered by the same open `doing/` action.
- Sleevenote (snapshot current, 6d): all 5 next_actions still covered by `actions/backlog/2026-06-26-three-initiatives-next-steps.md`, gated on the same identity-sentence decision as the content engine — nothing filed, same call as last run.
- Fadwa: 2 additional next_actions surfaced (Circa Arts follow-up, content direction) already match **done** actions filed 2026-06-22 (`circa-arts-joseph-intro-followup.md`, `fadwa-define-content-direction.md`) — skipped per stale-snapshot guard (37d), folded as new evidence into Q5 rather than opening a new question.
- Family: same pattern — its 3 next_actions all match done actions filed 2026-06-22 — folded as new evidence into Q3 with a lighter-weight resolution option (just clear them) rather than asking Dan to write fresh content.
- Growify rotting actions (`growify-brand-context-map`, `growify-posthog-review`, `growify-team-context-fields`, `growify-zoho-timeline`, 19d) and the 3 growify-brain-dump items (27d): already re-stamped earlier today, no change this pass.
- Fadwa rotting actions (`fadwa-send-june-session-dates`, `send-fadwa-white-paper`, 37d): still Dan's call, already queued (Q5) — left as-is.
- `[cohere.orphan_meeting]` "context": false positive — `meetings/context.md` is the workspace context file, not a meeting — skipped, not queued.
- `[cohere.orphan_meeting]` `2025-06-05-growify-ontology`: unchanged from earlier today — still queued (Q7), no new information to resolve it with.

### Queued for interview
- DPL gap — 7 of last 14 days unlogged, biggest lever on the health score (Q1, unchanged)
- Content engine — identity-sentence decision blocking restart, now also gating Sleevenote's next_actions (Q2, enriched)
- Family — 80d-stale snapshot; new evidence its 3 next_actions are already done (Q3, enriched)
- Santiago/Bonita — alive or dead, plus 66d-stale snapshot refresh (Q4, unchanged)
- Fadwa — chase overdue June session dates + white paper, plus 37d-stale snapshot; new evidence 2 more next_actions are already done (Q5, enriched)
- Shereen — refresh 39d-stale snapshot (Q6, unchanged)
- Orphan meeting `2025-06-05-growify-ontology` — confirm date before linking (Q7, unchanged)

## 2026-07-02 — /maintain (headless, CI)
**Health: 44/100** (was 44)

### Applied from interview
Nothing — all 7 questions in the open interview are still blank (no answer came back between runs). Not archived; carried forward unchanged into the same `_maintenance-interview.md` (content already correct, no rewrite needed).

### Auto-fixed
- Regenerated `_digest.md` (10 entities, unchanged from prior pass)
- Scanned `actions/{backlog,doing,done}/` for status/folder mismatches — none found
- `[cohere.index_drift]` — none flagged this run
- `[cohere.unused_ip]` 41 entries flagged, 0 older than 30d → nothing queued
- `[acct.ratio]` suppressed until 2026-07-06 per `scripts/.health-suppress.json` — skipped as designed

### Acted (judgment)
- Confirmed every decay/acct/coherence finding in this run's `_health.md` matches a decision already made and logged in the two passes earlier today (rotting-action re-stamps, quiet-entity coverage checks, stale-snapshot guards on Disha/Fadwa/Family/Santiago-Bonita/Shereen, Sleevenote/content-engine identity-sentence gate, orphan-meeting `context.md` false positive) — no new state, nothing to re-decide.
- Score unchanged (44/100) confirms no drift since the last pass — this run is a clean no-op confirmation, not a fresh finding set.

### Queued for interview
Unchanged — same 7 questions (Q1–Q7) as the prior pass, still awaiting Dan's answers. See `_maintenance-interview.md`.

## 2026-07-05 — /maintain (headless, CI)
**Health: 41/100** (was 42)

### Applied from interview
Nothing — all 7 questions from 2026-07-02's interview are still blank, 3 days later. Not archived (fully-blank interview); carried forward with enrichment into the same `_maintenance-interview.md`.

### Auto-fixed
- Regenerated `_digest.md` (10 entities)
- Scanned `actions/{backlog,doing,done}/` for status/folder mismatches — none found
- `[cohere.index_drift]` — none flagged; `index.md` dates match every snapshot's `last_updated`
- `[cohere.unused_ip]` 41 entries flagged, 0 older than 30d → nothing queued
- `[acct.ratio]` suppressed until 2026-07-06 per `scripts/.health-suppress.json` — skipped as designed

### Acted (judgment)
- Growify rotting actions — all 7 re-stamped as still relevant against the current (6d) Growify snapshot: 3 brain-dump items (`2026-06-05-growify-book-chandika-rohit-sessions`, `2026-06-05-growify-send-assets-and-brief`, `2026-06-05-growify-test-image-and-ad-workflows`, now 30d — Chandika/Rohit sessions and Disha's assets are still open tensions/next_actions per `entities/people/growify.md`) and 4 session-1 items (`growify-brand-context-map`, `growify-posthog-review`, `growify-team-context-fields`, `growify-zoho-timeline`, now 22d — folder-structure build and PostHog/Zoho decisions still open, nothing in the session-2 update resolves them)
- Growify: "Book Disha session" next_action already covered by open `growify-second-sessions-rishab-disha.md` — logged, nothing filed
- Jamie Cameron (snapshot current, 20d — right at the guard threshold): next_action "Chase Jamie for Social Trait update" matches the exact title of a **done** action (`jamie-chase-social-trait.md`) — snapshot's next_actions list wasn't cleaned up after that action closed, but the work itself is covered, so skipped rather than double-filed. Quiet-entity check covered by open `jamie-next-engagement.md` (doing).
- Sleevenote (snapshot current, 9d): all 5 next_actions still covered/gated by `actions/backlog/2026-06-26-three-initiatives-next-steps.md`, same identity-sentence block as Q2 — nothing filed, no change from last run
- Disha Bhatnagar: snapshot is 30d stale (over the 21d guard) — her 2 unfiled next_actions stay unfiled. New this run: her snapshot names today, 2026-07-05, as her return date from leave, so the staleness is no longer just "wait it out" — it's now actionable. Queued fresh rather than guessed, since only Dan knows whether the session actually happened.
- Fadwa, Family, Santiago/Bonita, Shereen: quiet-entity checks all covered by existing open actions (or already correctly queued as ambiguous, in Santiago/Bonita's case) — no change from last run, carried forward
- `[cohere.orphan_meeting]` "context": false positive — `meetings/context.md` is the workspace context file, not a meeting — skipped, not queued
- `[cohere.orphan_meeting]` `2025-06-05-growify-ontology`: unchanged, still queued — no new information to resolve the date question
- DPL gap: grew from 7 to 10 of the last 14 days unlogged (3 more days slipped since the last run) — question enriched with the new date list, not re-asked as new

### Queued for interview
- DPL gap — now 10 of last 14 days unlogged, biggest lever on the health score (Q1, enriched)
- Content engine — identity-sentence decision blocking restart, still gating Sleevenote (Q2, unchanged)
- Disha Bhatnagar — 30d-stale snapshot; her named return date (2026-07-05) is today, has the session happened? (Q3, new)
- Family — 83d-stale snapshot; 3 next_actions already done (Q4, unchanged)
- Santiago/Bonita — alive or dead, plus 69d-stale snapshot refresh (Q5, unchanged)
- Fadwa — chase overdue June session dates + white paper, plus 40d-stale snapshot (Q6, unchanged)
- Shereen — refresh 42d-stale snapshot (Q7, unchanged)
- Orphan meeting `2025-06-05-growify-ontology` — confirm date before linking (Q8, unchanged)

## 2026-07-12 — /maintain (headless, CI)
**Health: 46/100** (was 28)

### Applied from interview
Nothing — all 8 questions from the 2026-07-05 interview are still blank. Not archived (fully-blank interview); resolved most of them directly this run using new snapshot evidence (see below) and carried the genuine leftovers forward into a refreshed `_maintenance-interview.md`.

### Auto-fixed
- Regenerated `_digest.md` (11 entities)
- Scanned `actions/{backlog,doing,done}/` for status/folder mismatches — none against the done/backlog/doing rule (3 files carry non-standard `pending`/blank `status` values, out of scope for mechanical reconciliation, left as-is)
- `[cohere.index_drift]` — none flagged this run
- `[cohere.unused_ip]` 41 entries flagged, 0 older than 30d → nothing queued
- `[acct.ratio]` suppression (`scripts/.health-suppress.json`, expired 2026-07-06) no longer applies — ratio now live: 0.64, above the 0.5 floor, logged only

### Acted (judgment)
- **Four stale snapshots from the old interview turned out to have been refreshed since 2026-07-05** (Fadwa, Family, Santiago/Bonita, Shereen all now ≤9d old) — re-checked each against the STALE-SNAPSHOT GUARD fresh rather than trusting the old interview's staleness numbers:
  - Disha Bhatnagar (now 3d): filed 2 of 5 unfiled next_actions (`disha-confirm-posthog-decision.md`, `disha-rishabh-reporting-alignment.md`); rest covered by `growify-second-sessions-rishab-disha.md`. Resolves old Q3 — session context is current.
  - Fadwa (now 3d, refreshed since Circa Arts news landed): filed `fadwa-await-scheduling-reply.md` and `fadwa-confirm-session.md`; `£80/month billing` next_action already covered by existing `set-up-80-month-billing.md`. Dropped `fadwa-send-june-session-dates.md` to `done/` as superseded — the current snapshot shows Dan chasing a new general catch-up, not the old June-specific ask.
  - Family (now current): 3 of its 4 next_actions already matched **done** actions (`family-childcare-conversation.md`, `family-plan-date-night.md`, `family-household-prep-august.md`) — cleared from the snapshot's `next_actions` and bumped `last_updated`; filed the 4th (`family-finance-tracker-notion.md`). Fully resolves old Q4.
  - Shereen (now current): all 3 unfiled next_actions already covered by the existing `shereen-confirm-scope.md` — logged covered, nothing filed. Fully resolves old Q7.
  - Santiago/Bonita (now current, no longer stale): its one next_action is the alive-or-dead decision itself, not an executable task — left unfiled. Snapshot's own language now leans harder toward "stalled" (both live-project lines confirmed cancelled/archived) but still stops short of a decision — re-queued with the new detail (Q3 below).
- Sam / Explorers Club (current, 1d): filed `sam-schedule-catchup-call.md`; the other next_action already covered by existing Notion-setup/hike-brief actions.
- Jamie Cameron (current, 1d): filed `jamie-catchup-week-0714.md` (due 2026-07-14) and a fresh `jamie-chase-social-trait-2.md` — the 2026-06-22 chase (`jamie-chase-social-trait.md`) is closed and the situation is unchanged per Jamie's 2026-07-11 snapshot, so this is a new chase cycle, not a duplicate. Third next_action already covered by `jamie-next-engagement.md`.
- Victoria Russel (current, 3d): filed both unfiled next_actions (`victoria-log-upcoming-meeting.md`, `victoria-clarify-venture-scope.md`) — new entity to the maintenance loop, no prior coverage.
- Sleevenote (current, 16d): filed all 5 next_actions as individual backlog actions. Re-examined the prior runs' link between Sleevenote and the "content engine identity-sentence" parked thread (old Q2) — `self/goals.md` lists them as adjacent but unconnected bullets, and Sleevenote's next steps (pitch deck, influencer outreach, 3D clip) don't actually depend on DAN's own brand-identity sentence. Released the gate; Q2 below now covers only DAN's own content engine.
- DoAnythingNow (current, 9d): filed `doanythingnow-integrate-3d-logo.md`; other 2 next_actions already covered by existing outreach/Growify-Phase-2 actions.
- Rotting actions re-stamped as still relevant against Growify's 2026-07-09 snapshot: `growify-brand-context-map`, `growify-posthog-review`, `growify-team-context-fields`, `growify-zoho-timeline`, `2026-06-05-growify-book-chandika-rohit-sessions` (Chandika/Rohit still named as an open tension, deferred not cancelled).
- `2026-06-05-growify-send-assets-and-brief` (37d): partial progress — Disha's snapshot confirms raw images + specs were sent, ad brief + sample report unconfirmed — left in backlog, stamp updated.
- `2026-06-05-growify-test-image-and-ad-workflows` (37d): moved `backlog/` → `doing/` — Disha's snapshot directly states "Daniel researching PostHog and testing workflows."
- `send-fadwa-white-paper` (47d): still no evidence either way on whether editing is complete — left in place, re-queued (Q4 below, narrower than old Q6 now that the June-session half is resolved).
- `[decay.quiet_entity]` Sleevenote: resolved via the 5 filed actions above — covered.
- `[decay.parked_thread]` Content engine (`self/goals.md`): still stalled, no evidence the identity-sentence decision has been made — real strategic choice, left in place, re-queued (Q2).
- `[decay.dpl_gap]` 13 of last 14 days unlogged, up from 10 three days ago — re-queued with the current date list (Q1).
- `[cohere.orphan_meeting]` "context": false positive — `meetings/context.md` is the workspace context file, not a meeting — skipped, not queued.
- `[cohere.orphan_meeting]` `2025-06-05-growify-ontology`: unchanged, no new evidence — re-queued (Q5).

### Queued for interview
- DPL gap — now 13 of last 14 days unlogged, biggest lever on the health score (Q1)
- Content engine — identity-sentence decision blocking restart (Q2, narrowed — no longer gates Sleevenote)
- Santiago/Bonita — alive or dead; snapshot now leans "stalled" but still needs Dan's call (Q3, enriched)
- `send-fadwa-white-paper` — still live or drop, now that the June-session half of the old question is resolved (Q4, narrowed)
- Orphan meeting `2025-06-05-growify-ontology` — confirm date before linking (Q5, unchanged)

Interview shrank from 8 open questions to 5 — four resolved outright this run on fresh snapshot evidence (Disha, Family, Shereen, plus the superseded Fadwa June-session action).

## 2026-07-19 — /maintain
**Health: 45/100** (was 45)

### Applied from interview
Nothing — the 2026-07-12 interview (5 questions) is still fully blank. Not archived per the fully-blank rule; all 5 questions carried forward into the refreshed `_maintenance-interview.md` (some with updated day counts/evidence).

### Auto-fixed
- `index.md` — corrected Family date column 2026-07-03 → 2026-07-12 to match snapshot `last_updated`
- Scanned `actions/{backlog,doing,done}/` for status/folder mismatches — none against the backlog/doing/done rule (3 files carry non-standard `pending`/blank `status` values — `create-workshop-visuals.md`, `update-skool-visuals.md`, `2026-06-26-three-initiatives-next-steps.md` — out of scope for mechanical reconciliation, left as-is)
- `[cohere.unused_ip]` 41 entries flagged `content_made:false`, 0 older than 30d → nothing queued
- Regenerated `_digest.md` (11 entities)

### Acted (judgment)
- 11 Growify rotting backlog actions re-confirmed still relevant against Growify's 2026-07-09 snapshot `next_actions` — appended dated stamps, left in place: `2026-06-05-growify-book-chandika-rohit-sessions`, `2026-06-05-growify-send-assets-and-brief`, `growify-brand-context-map`, `growify-dan-build-self-folders`, `growify-dan-hermes-setup`, `growify-dan-migrate-workflowy-airtable`, `growify-posthog-review`, `growify-rishab-send-airtable`, `growify-rishab-send-workflowy`, `growify-team-context-fields`, `growify-zoho-timeline`
- `2026-06-05-growify-test-image-and-ad-workflows` (44d in doing/, no notes update since moving in 2026-07-12) — flagged stale, appended comment, queued for Dan's call (Q6)
- `[decay.quiet_entity]` DoAnythingNow — covered: open actions already exist (`doanythingnow-integrate-3d-logo.md`, `growify-phase-2-proposal.md`), nothing filed
- `[decay.quiet_entity]` Sleevenote — covered: 5 open backlog actions already exist from the prior run, nothing filed
- `[acct.unfiled_next_action]` Santiago/Bonita "Decide: revive or lapse" — not filed, it *is* the decision already queued as Q3; filing it as a task would just duplicate the interview question
- `[acct.unfiled_next_action]` Shereen "If deposit lands, confirm start date" — skipped, already covered (loose match) by existing `shereen-confirm-scope.md`
- `[acct.unfiled_next_action]` Shereen "Keep chasing weekly if no response" — not covered by an existing action, filed `shereen-keep-chasing-weekly.md`
- `[acct.ratio]` Commit→done last 7d: 38 created / 15 done (0.39) — below the 0.5 floor, logged and queued (Q4)
- `[cohere.orphan_meeting]` "context" — false positive, `meetings/context.md` is the workspace context file (per CLAUDE.md), not a meeting record — skipped, not queued
- `[cohere.orphan_meeting]` `2025-06-05-growify-ontology` — unchanged, no new evidence — re-queued (Q7)
- `[decay.parked_thread]` Content engine — still stalled, no evidence the identity-sentence decision has been made — re-queued (Q2)
- `[decay.dpl_gap]` now 14 of last 14 days unlogged (up from 13/14) — re-queued with current date list, still the single biggest lever on the score (Q1)

### Queued for interview
- DPL gap — 14/14 days unlogged, biggest lever on the health score (Q1, updated)
- Content engine — identity-sentence decision still blocking restart (Q2, unchanged)
- Santiago/Bonita — alive or dead (Q3, unchanged)
- Commit→done ratio 0.39 — backlog growing faster than it clears; block time to clear it down? (Q4, new)
- `send-fadwa-white-paper` — still live or drop, now 54d (Q5, updated)
- `2026-06-05-growify-test-image-and-ad-workflows` stale in doing/ 44d — finish or move back to backlog? (Q6, new)
- Orphan meeting `2025-06-05-growify-ontology` — confirm date before linking (Q7, unchanged)

Score held flat at 45 for the third straight run. The DPL gap is now total — every day of the last two weeks is unlogged — and is the dominant driver keeping the score from moving. Everything else this run was confirmation and light filing; no new decay categories emerged.

## 2026-07-26 — /maintain
**Health: 24/100** (was 30)

### Applied from interview
Nothing — the 2026-07-19 interview (7 questions) is still fully blank. Not archived per the fully-blank rule; all 7 questions carried forward into the refreshed `_maintenance-interview.md` with updated day counts/evidence.

### Auto-fixed
- Scanned `actions/{backlog,doing,done}/` for status/folder mismatches — none against the backlog/doing/done rule (the same 3 non-standard files — `create-workshop-visuals.md`, `update-skool-visuals.md` (`status: pending`), `2026-06-26-three-initiatives-next-steps.md` (no status field) — remain out of scope for mechanical reconciliation, left as-is)
- `[cohere.unused_ip]` 41 entries flagged `content_made:false`, 0 older than 30d → nothing queued
- Regenerated `_digest.md` (11 entities)

### Acted (judgment)
- 10 Growify rotting backlog actions re-confirmed still relevant against Growify's 2026-07-09 snapshot `next_actions` — appended dated stamps, left in place: `2026-06-05-growify-book-chandika-rohit-sessions` (51d), `2026-06-05-growify-send-assets-and-brief` (51d), `growify-brand-context-map` (43d), `growify-dan-build-self-folders` (27d), `growify-dan-hermes-setup` (27d), `growify-dan-migrate-workflowy-airtable` (27d), `growify-posthog-review` (43d), `growify-rishab-send-airtable` (27d), `growify-rishab-send-workflowy` (27d), `growify-team-context-fields` (43d), `growify-zoho-timeline` (43d)
- `[decay.quiet_entity]` Disha, Sam/Explorers Club, Fadwa, Growify, Jamie Cameron, Shereen, Victoria Russel, Sleevenote, DoAnythingNow — all covered: each already has one or more open backlog/doing actions addressing re-engagement, nothing new filed
- `[decay.quiet_entity]` Santiago/Bonita — not covered; this is the dead-vs-alive call already queued as Q3, no check-in action fabricated
- `[acct.unfiled_next_action]` Santiago/Bonita "Decide: revive or lapse" — not filed, it *is* the decision already queued as Q3; filing it as a task would just duplicate the interview question
- `[acct.unfiled_next_action]` Shereen "If deposit lands, confirm start date" — skipped, already covered (loose match) by existing `shereen-confirm-scope.md`
- `[acct.ratio]` Commit→done last 7d: 39 created / 15 done (0.38, down from 0.39) — still below the 0.5 floor, logged and re-queued (Q4)
- `[cohere.orphan_meeting]` "context" — false positive, `meetings/context.md` is the workspace context file (per CLAUDE.md), not a meeting record — skipped, not queued
- `[cohere.orphan_meeting]` `2025-06-05-growify-ontology` — unchanged, no new evidence — re-queued (Q7)
- `[decay.parked_thread]` Content engine — still stalled per `self/goals.md`, no evidence the identity-sentence decision has been made — re-queued (Q2)
- `[decay.rotting_action]` `send-fadwa-white-paper` — now 61d (up from 54d), no new evidence either way — re-queued, no comment appended (Q5)
- `[decay.stale_doing]` `2026-06-05-growify-test-image-and-ad-workflows` — now 51d in doing/ (up from 44d), still no notes update — re-queued (Q6)
- `[decay.dpl_gap]` now 14 of last 14 days unlogged, window fully rolled forward (2026-07-13 → 2026-07-26) — re-queued with current date list, still the single biggest lever on the score (Q1)

### Queued for interview
- DPL gap — 14/14 days unlogged, biggest lever on the health score (Q1, updated)
- Content engine — identity-sentence decision still blocking restart (Q2, unchanged)
- Santiago/Bonita — alive or dead (Q3, unchanged)
- Commit→done ratio 0.38 — backlog growing faster than it clears; block time to clear it down? (Q4, updated — third consecutive run below floor)
- `send-fadwa-white-paper` — still live or drop, now 61d (Q5, updated)
- `2026-06-05-growify-test-image-and-ad-workflows` stale in doing/ 51d — finish or move back to backlog? (Q6, updated)
- Orphan meeting `2025-06-05-growify-ontology` — confirm date before linking (Q7, unchanged)

Score dropped from 30 to 24 — the third straight run with no forward movement, driven almost entirely by the DPL gap going total (every day of the last two weeks unlogged) and the commit→done ratio sliding further below floor (0.39 → 0.38). No new decay categories emerged; everything else this run was re-confirmation and light coverage-checking. The interview is unchanged in shape (7 questions) but every question is now more expensive to leave unanswered than last week.

## 2026-08-02 — /maintain
**Health: 38/100** (was 38)

Run headless via `self-heal.yml`; the 2026-07-26 interview was fully blank (Dan was away ~3 weeks per `self/goals.md` — house prep for baby #2), so per Step 0 it was skipped rather than archived and this run re-derived fresh findings from current state instead of blindly carrying forward stale questions.

### Auto-fixed
- `[cohere.index_drift]` Jamie Cameron — `index.md` dated 2026-07-11, snapshot `last_updated` 2026-07-20 → `index.md` corrected
- Scanned `actions/{backlog,doing,done}/` for status/folder mismatches — none found, all frontmatter matches folder placement
- `[cohere.unused_ip]` 43 entries flagged `content_made:false`, 0 older than 30d → nothing queued
- Regenerated `_digest.md` (11 entities)

### Acted (judgment)
- `[decay.quiet_entity]` Family — already covered by open action `check-in-family.md`, nothing new filed
- `[decay.quiet_entity]` Santiago/Bonita — already resolved: snapshot `current_state` (refreshed 2026-07-13) and `self/goals.md` both record it as archived/closed. The old Q3 ("alive or dead?") is stale noise from before that resolution landed — not re-queued
- `actions/backlog/2026-06-05-growify-book-chandika-rohit-sessions.md` → dropped to `done/` — Growify's 2026-07-28 snapshot confirms the pilot scope was narrowed to Rishab + Disha only, Chandika/Rohit deferred; the open question survives as a tension in `entities/people/growify.md`, not lost
- `actions/backlog/growify-posthog-review.md` → dropped to `done/` — duplicate of `disha-confirm-posthog-decision.md`, which already tracks the same open PostHog decision; neither Growify's nor Disha's 2026-07-28 snapshot mentions PostHog anymore
- `actions/backlog/jamie-raise-ai-pods-workshop-social-trait.md` → dropped to `done/` — the 3pm call it tracked (due 2026-07-20) has already happened; the live follow-up thread is already covered by `jamie-catchup-and-social-trait-chase.md` and `jamie-chase-social-trait-2.md`
- 12 other rotting backlog actions re-confirmed still relevant against fresher 2026-07-28 (Growify) / 2026-07-20 (Jamie) snapshots — appended dated stamps, left in place: `2026-06-05-growify-send-assets-and-brief` (58d, blocked on unresponsive Disha), `growify-brand-context-map` (50d), `growify-team-context-fields` (50d), `growify-dan-build-self-folders` (34d), `growify-dan-hermes-setup` (34d), `growify-dan-migrate-workflowy-airtable` (34d), `growify-rishab-send-airtable` (34d), `growify-rishab-send-workflowy` (34d), `2026-07-13-carousel-templates-system` (37d), `2026-07-13-sleevenote-pitch-deck-prep` (37d), `2026-07-13-website-identity-distillation` (37d, explicitly deferred per goals.md), `jamie-email-meeting-summary-action-items` (13d, 11d past due), `jamie-notion-ai-assistant-mvp-spec` (13d), `jamie-pitch-deck-smb-enterprise-ai` (13d)
- `[decay.stale_doing]` `2026-06-05-growify-test-image-and-ad-workflows` (58d in doing/, no notes update since 2026-07-12) → moved back to `backlog/` — Disha's 2026-07-28 snapshot confirms she hasn't replied since 2026-07-14, so this is blocked, not actively in progress
- `[acct.unfiled_next_action]` Fadwa "Check in on how Circa Arts is landing" — filed `fadwa-checkin-circa-arts.md` (snapshot current, 2026-07-28)
- `[acct.unfiled_next_action]` Fadwa "Hold the final session — Friday 2026-07-31" — date has passed with no update; not filed as done or dropped, queued instead (Q3)
- `[acct.ratio]` Commit→done last 7d: 43 created / 17 done (0.40) — still below the 0.5 floor, fourth consecutive run below it — logged and re-queued (Q2)
- `[cohere.orphan_meeting]` `meetings/context.md` — false positive, this is the meetings/ folder's own context/README file (per CLAUDE.md), not a meeting record — skipped, not queued
- `[decay.rotting_action]` `growify-zoho-timeline` (50d) — absent from Growify's current_focus/next_actions/tensions for three consecutive snapshot refreshes; genuinely ambiguous whether it's still live — queued rather than guessed (Q4)
- `[decay.dpl_gap]` still 14 of last 14 days unlogged, window fully rolled forward to 2026-07-20 → 2026-08-02 — re-queued, still the single biggest lever on the score (Q1)

### Queued for interview
- DPL gap — 14/14 days unlogged, fourth straight run fully blank (Q1)
- Commit→done ratio 0.40 — fourth consecutive run below floor, backlog flat at 53 (Q2)
- Fadwa's final session (Friday 2026-07-31) — did it happen? (Q3, new)
- `growify-zoho-timeline` — still live or drop? (Q4, new)

Entered this run at 38 (unchanged from 2026-07-26 — the interview went completely unanswered while Dan was off the business for ~3 weeks). This run's job was mostly re-grounding stale "still relevant" reasoning in fresher 2026-07-28 snapshot data rather than genuinely new progress, but the cleanup moved the needle: re-running `system_health.py` after fixes shows **51/100**. Three rotting/duplicate actions dropped outright (Chandika/Rohit booking, PostHog duplicate, the passed Social Trait call), one stalled doing/ item correctly moved back to backlog instead of being left to rot in place, and the index drift + digest are current again. The interview shrank from 7 questions to 4 — the identity-sentence and Santiago/Bonita questions resolved themselves via decisions already recorded elsewhere in the vault. What's left is genuinely Dan's call: the DPL gap and the accountability ratio are both now four runs deep with zero response, and both cost more the longer they sit unanswered.
