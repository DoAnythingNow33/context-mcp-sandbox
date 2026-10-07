# Hermes — Infrastructure

Where the always-on Hermes assistant actually runs, and what's installed on the box.

## Server

| Field | Value |
|-------|-------|
| Provider | Hetzner |
| Hostname | `dan-hermes-assitant` |
| SSH alias | `hermes` (configured in `~/.ssh/config` on the Mac — `ssh hermes` connects directly) |
| IPv4 | `5.75.188.204` |
| OS | Ubuntu 26.04 LTS |
| Specs | 2 vCPU (AMD EPYC-Rome), 3.7GB RAM, 38GB disk |
| Login user | `root` |

The box is small — keep that in mind before installing anything RAM-hungry (heavier local models, GPU-oriented tooling, etc). ~3GB of the 3.7GB is reclaimable buff/cache, not hard-committed, but don't assume headroom for anything beyond lightweight local tools.

## Multi-tenant instances (live registry)

As of 2026-07-29, this box runs more than one Hermes gateway, each fully isolated by Linux user. Keep this table current — it's the fastest way to answer "what's actually running here" without SSHing in. Full setup process: `multi-tenant-setup-sop.md`.

| Linux user | Client | Discord app | Systemd unit | Context repo | Model | Billing key |
|---|---|---|---|---|---|---|
| `hermes` | Dan (primary) | Dan's personal Hermes | `hermes-gateway.service` | `~/context-2.0-github` | conversational `claude-haiku-4.5` + delegation `claude-sonnet-5`, direct via Anthropic API. Haiku on the conversational slot is a deliberate credit-stretching choice (confirmed 2026-08-25) — short capture turns don't need a frontier model, delegated work still gets Sonnet. | Dan's own `ANTHROPIC_API_KEY` |
| `rishab` | Growify | "Growify Assistant" | `hermes-gateway-rishab.service` | `~/growify-context` | `anthropic/claude-sonnet-5` via OpenRouter (both conversational + delegation — switched 2026-07-29 off the Haiku/Sonnet split, matching Dan's own single-model setup) | separate `Rishab-Agent` OpenRouter key, credit-capped — see `troubleshooting.md` for the recurring account-balance 402 |

Each instance's unit file must be hand-written and distinctly named — `hermes gateway install --system --run-as-user <x>` always targets the same fixed path and will silently overwrite whatever's already there. See `troubleshooting.md` → "Multi-tenant gateway install clobbers the wrong unit file."

**The Hetzner box is the only place a gateway should run.** Confirmed 2026-07-29/30: a leftover local gateway on Dan's own Mac (launched via `launchd`, `~/Library/LaunchAgents/ai.hermes.gateway.plist`) had been quietly running in parallel with `hermes-gateway.service` on the box, both holding Dan's same `DISCORD_BOT_TOKEN` — caused every Discord message to get two replies. Unloaded (`launchctl unload -w ...`) but the plist file itself is still present on the Mac, just not loaded — delete it outright to guarantee it can't auto-start again on next login/reboot. See `troubleshooting.md` → "Bot replies twice to every message."

## What's installed

| Component | Location | Notes |
|-----------|----------|-------|
| Hermes Agent | `/usr/local/lib/hermes-agent` (venv-based) | v0.18.0 at time of writing. Config at `~/.hermes/config.yaml`, secrets in `~/.hermes/.env` |
| Hermes gateway | systemd **system** service `hermes-gateway.service` at `/etc/systemd/system/hermes-gateway.service` | Confirmed 2026-07-29 (a prior version of this doc wrongly called it a user-level unit — `README.md` had the right answer). Restarting always needs `sudo`/`ssh hermes-root`, even though it runs *as* `hermes`. Restart: `ssh hermes-root "systemctl restart hermes-gateway.service"` |
| Context 2.0 repo | `~/context-2.0-github` | Cloned copy Hermes reads/writes and syncs over SSH to GitHub. `ssh hermes` auto-`cd`s here on interactive login (snippet in `~/.bashrc`) — same `CLAUDE.md` as the Mac vault, so a `claude` session started here auto-loads project context |
| Claude Code CLI | `/usr/local/bin/claude` (npm global) | Installed 2026-07-03. Auth: **subscription login** (`claude login`, browser step done on your phone/laptop, not the server) — bills your Pro/Max plan, not the Anthropic API key. An earlier auto-exported `ANTHROPIC_API_KEY` env var was removed from `~/.bashrc` on 2026-07-03 because it silently overrides subscription login and would bill the API key instead. |
| ffmpeg | `/usr/bin/ffmpeg` | Required for TTS/voice-message audio conversion (Telegram opus bubbles etc) |
| Node | v22.23.1 | |
| Python | 3.11.15 inside the Hermes venv; 3.14.4 is the system default | Hermes always runs from its own venv — don't assume system `python3`/`pip3` see its packages (no system `pip3` binary at all) |

## TTS / STT setup — superseded 2026-07-29

`tts.provider` was originally `edge` (free, unofficial Microsoft endpoint — see history below), then upgraded to `openai` (`gpt-4o-mini-tts`, voice `alloy`) on both `hermes` and `rishab` instances, priced ~3x cheaper than ElevenLabs and without Edge's unofficial-endpoint risk. `stt.provider` moved from the unconfigured default (local `faster-whisper`, model `base` — weak accuracy on this box's 2 vCPU) to `groq` (`whisper-large-v3`, hosted, offloads compute, noticeably more accurate). Both changes require the `model:` field explicitly set on the `openai` TTS block — it's easy to omit and the failure is silent (falls back to text replies with no error logged). See `config-reference.md` for the live config block.

**Original TTS history (2026-07-03):** `tts.provider` was switched from `openai` → `edge`. `openai` was pre-configured but `VOICE_TOOLS_OPENAI_KEY` was never set in `.env`, so TTS silently failed. Local heavy engines (Coqui/XTTS) were ruled out — this box doesn't have the RAM/CPU headroom. Piper (local, CPU-only) was considered as the safe local fallback, but Edge TTS was chosen instead: free, no key, and noticeably more natural (Azure neural voices) than Piper's robotic local synthesis. Superseded by the OpenAI switch above once a real `VOICE_TOOLS_OPENAI_KEY` was set.

## Handling secrets on this box

`~/.hermes/.env` holds live API keys (Anthropic, OpenRouter, Discord bot token, Telegram bot token, etc). Rules when working on this server:

- Never copy values out of `.env` into this vault, a chat log, or any file that syncs to GitHub. Reference *where* a secret lives, never the value itself.
- Hermes itself refuses to let its own agent read or patch `.env` / `config.yaml` directly (defense-in-depth) — those files must be edited by hand over SSH, not through Hermes's own tools.
