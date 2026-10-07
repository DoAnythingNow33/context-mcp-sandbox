---
title: "Set up Hermes pipeline for Rishab (Telegram or Discord)"
owner: Dan
due: "2026-07-29"
status: done
source: "[[2026-06-29-growify-session-2]]"
---

## Notes

Discord confirmed (not Telegram) — matches Dan's own current stack. Full build steps: [[hermes/multi-tenant-setup-sop]]. Proposal to present alongside it: [[entities/projects/offers/growify-ai-assistant-proposal]].

**Built and live, 2026-07-29** — same day as the catch-up call. "Growify Assistant" Discord bot running on its own systemd service (`hermes-gateway-rishab`) under a dedicated `rishab` Linux user on Dan's Hetzner box, colocated with Dan's own Hermes without disturbing it. Reads the real Growify context folder (existing Google-Drive-synced vault, migrated to a new private GitHub repo `growify-context`). Both Dan's and Rishab's Discord IDs allowlisted; tested working end-to-end before the call. Separate OpenRouter key for Growify billing separation.

**2026-07-29/30 follow-up — model collapsed to Sonnet 5:** both Dan's instance and Growify's now run `claude-sonnet-5` for both conversational + delegation, matching each other. Dan direct via the Anthropic API (own key); Growify via the OpenRouter key (`Rishab-Agent`) — Dan topped up the OpenRouter account balance ($5) after an earlier 402 from the account running down to $0.29. Also found and fixed: a leftover local Hermes gateway on Dan's own Mac (`launchd`, unrelated to Growify but shares the same box/session) was double-replying to Dan's own bot on Discord — unloaded, see `hermes/troubleshooting.md`.

<!-- /maintain 2026-07-19: rotting (20d) — still relevant, confirmed against Growify's 2026-07-09 snapshot next_actions, left in place -->
<!-- /maintain 2026-07-26: rotting (27d) — still relevant, confirmed against Growify's 2026-07-09 snapshot next_actions, left in place -->
<!-- /maintain 2026-08-02: rotting (34d) — still relevant, matches the "Joint Hermes setup session with Rishab + Disha" next_action in Growify's 2026-07-28 snapshot, left in place -->
<!-- /maintain 2026-08-09: rotting (41d) — still relevant, matches "Joint Hermes setup session with Rishab + Disha" in Growify's 2026-07-28 snapshot next_actions (current, 12d), left in place -->
<!-- /maintain 2026-08-16: dropped — the note body already describes the build as shipped and tested end-to-end (2026-07-29) plus a completed follow-up (2026-07-30); no longer appears in Growify's current 2026-07-30 snapshot current_focus/next_actions — marked done -->
