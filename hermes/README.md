# Hermes — Reference Hub

Hermes is Dan's always-on AI assistant. SSH access to the Context 2.0 GitHub repo. Handles morning/evening debriefs and ad-hoc capture throughout the day.

## Files in this folder

| File | Purpose |
|------|---------|
| `infrastructure.md` | Where the box actually lives (Hetzner, IP, SSH alias, specs) + what's installed on it, plus a live registry of every client instance running |
| `config-reference.md` | Working config snippets — copy/paste to `config.yaml` on the Hermes machine — plus the `SOUL.md` rooting pattern |
| `multi-tenant-setup-sop.md` | Step-by-step SOP for onboarding a new client as a colocated, isolated Hermes instance (own Linux user, Discord bot, context repo, billing key) — the repeatable process, pitfalls folded in from the first real run |
| `troubleshooting.md` | Diagnostic runbook — what to check when things are slow or broken, including client-instance-specific failure modes |
| `tts-discord-setup.md` | Getting TTS (text-to-speech) working on the Discord bot — install, config.yaml, intents, rollout order |

## Vault docs (the operating manual)

| File | Purpose |
|------|---------|
| `docs/hermes-setup.md` | What each scheduled message does (morning/evening debrief logic) |
| `docs/hermes-capture.md` | Routing rules for ad-hoc inputs — where everything goes |

## Quick links

- Hermes Agent docs: https://hermes-agent.nousresearch.com
- OpenRouter models: https://openrouter.ai/models
- Discord Developer Portal: https://discord.com/developers/applications

## Current stack

| Layer | Choice |
|-------|--------|
| Platform | Discord |
| Primary model (conversational) | `claude-haiku-4.5` direct via Anthropic API — **deliberate, to stretch available credits**. Most Discord turns are short capture/routing exchanges that don't need a frontier model. Confirmed against live `config.yaml` 2026-08-25. |
| Delegation model (task/tool-use) | `claude-sonnet-5` direct via Anthropic API — real work still gets the stronger model. The two-tier split is intentional, not drift. |
| TTS | OpenAI (`gpt-4o-mini-tts`, voice `alloy`) — switched 2026-07-29 off Edge TTS, see `config-reference.md` |
| STT | Groq (`whisper-large-v3`) — switched 2026-07-29 off local `faster-whisper` |
| Repo sync | GitHub over SSH |
| Hosting | Hetzner, `ssh hermes` — see `infrastructure.md` |

> Source of truth for the above is `~/.hermes/config.yaml` on the Hermes machine — if this table and the live config disagree, trust the config and fix this table.

## Install layout (on the Hermes machine)

Hermes Agent's code and its data/config are in two separate places — this matters if you're ever debugging why an edit "isn't taking effect":

| What | Where | Owned by |
|------|-------|----------|
| Source + Python venv (git-installed) | `/usr/local/lib/hermes-agent` | `hermes` |
| CLI binary | `/usr/local/bin/hermes` | `hermes` |
| Config, secrets, state — `config.yaml`, `.env`, `SOUL.md`, logs, sessions, skills, memories | `~/.hermes/` (i.e. `/home/hermes/.hermes/`) | `hermes` |
| Gateway service definition | `/etc/systemd/system/hermes-gateway.service` | root (system-level unit — restarting it always needs `sudo`, even though it runs *as* `hermes`) |

The gateway runs as a systemd **system** service (`hermes gateway install --system --run-as-user hermes`), not a bare process and not a user-level unit — that's what makes it survive reboots without needing `loginctl enable-linger`. Confirmed 2026-07-29 (this table's row already had it right; `infrastructure.md` briefly disagreed and has been fixed). To restart after a config change: `ssh hermes-root "systemctl restart hermes-gateway.service"` — same-length equivalent to `sudo hermes gateway restart --system` run locally on the box.

**If you ever find the gateway not picking up config changes:** run `hermes config path` as both `root` and as `hermes` — if they print different paths, there are two separate Hermes profiles and the wrong one is live. See `troubleshooting.md` → "Gateway split across root and hermes user" for the full diagnosis and fix.
