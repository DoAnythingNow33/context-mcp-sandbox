# Hermes Config Reference

Working config snippets for `config.yaml` on the Hermes machine.
Copy sections as needed — don't paste the full file blindly, adapt to what Hermes already has.

**As of 2026-07-29, confirmed against Dan's own live `config.yaml`:** the real top-level schema is `model:` (conversational) + `delegation:` (task/tool-use model) — not the `inference:`-with-nested-`fallback:` shape shown in older drafts of this file. GLM 5.2 was evaluated at some point but is **not** the live model; correct as of now:

## Model — live schema (confirmed 2026-07-29)

Dan's own instance (`hermes` user) runs both slots on Claude Sonnet 5, direct via the Anthropic API — switched 2026-07-29 off Gemini Flash + OpenRouter after Dan found Gemini didn't understand context well and wanted to consolidate off a two-tier split:

```yaml
model:
  provider: anthropic
  default: claude-haiku-4.5   # conversational — deliberate, stretches credits
delegation:
  provider: anthropic
  model: claude-sonnet-5      # task/tool-use — real work gets the stronger model
```

**Updated 2026-08-25:** the conversational slot runs Haiku 4.5, not Sonnet 5.
This is intentional cost management, not drift — most Discord turns are short
capture/routing exchanges. Delegation stays on Sonnet 5 so actual work is
unaffected. An earlier version of this file claimed both slots ran Sonnet 5.

`api_key` isn't set inline — `ANTHROPIC_API_KEY` is picked up from `.env` by convention. Note the model ID has **no vendor prefix** here (`claude-sonnet-5`, not `anthropic/claude-sonnet-5`) — the `anthropic/` prefix is an OpenRouter routing convention, not part of the real Anthropic model ID.

Client instances (e.g. Growify/`rishab`) still route through OpenRouter, but as of 2026-07-29 also run Sonnet 5 for both slots — the Haiku/Sonnet split was collapsed to match Dan's own single-model setup:

```yaml
model:
  provider: openrouter
  default: anthropic/claude-sonnet-5
delegation:
  provider: openrouter
  model: anthropic/claude-sonnet-5
```

`model` handles conversational turns; `delegation` is used for actual task/tool-use work.

Always verify against the live file before reusing a snippet from this doc — see `hermes/README.md`: "Source of truth for the above is `~/.hermes/config.yaml` on the Hermes machine — if this table and the live config disagree, trust the config and fix this table." The same rule applies here.

---

## Platform — Discord

```yaml
messaging:
  platform: discord
  discord:
    token: "YOUR_DISCORD_BOT_TOKEN"
    allowed_users:
      - "YOUR_DISCORD_USER_ID"    # right-click your name → Copy User ID (needs Developer Mode on)
    require_mention: true         # gates server/guild channels only — DMs are always exempt
    free_response_channels: "*"   # "*" = no @mention needed anywhere; or list specific channel IDs.
                                   # Easy to forget when copying this skeleton — without it, every
                                   # server channel silently requires an @mention even if it didn't before.
```

**How to get your Discord User ID:**  
Settings → Advanced → enable Developer Mode → right-click your username anywhere → Copy User ID

**How to create the bot:**  
1. discord.com/developers/applications → New Application → name it "Hermes"
2. Bot tab → Add Bot → Reset Token → copy it
3. Privileged Gateway Intents → enable **Message Content Intent**
4. OAuth2 → URL Generator → scopes: `bot` → permissions: `Send Messages`, `Read Message History`
5. Open the generated URL in browser → add bot to your server

---

## Platform — Telegram (old, for reference)

```yaml
messaging:
  platform: telegram
  telegram:
    token: "YOUR_TELEGRAM_BOT_TOKEN"
    allowed_users:
      - YOUR_TELEGRAM_USER_ID
```

Keep this block commented out until Discord is confirmed working, then remove.

---

## TTS — OpenAI (current, as of 2026-07-29)

```yaml
tts:
  provider: "openai"
  openai:
    model: "gpt-4o-mini-tts"
    voice: "alloy"
```

`model:` is **required** — omitting it fails silently (falls back to text replies, no error in the gateway logs) rather than raising a config error. `voice` options: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`. Needs `VOICE_TOOLS_OPENAI_KEY` in `.env`. Chosen over Edge (see history below) and over ElevenLabs — roughly 3x cheaper per character than ElevenLabs' cheapest tier, official API (no unofficial-endpoint risk). Live on both `hermes` and `rishab`/Growify.

**Previously — Edge TTS (2026-07-03 → 2026-07-29):**

```yaml
tts:
  provider: "edge"
  edge:
    voice: en-US-AriaNeural
```

Free, no API key, no local model download — routed through Microsoft's `edge-tts` package. Superseded by the OpenAI switch above. Still a viable fallback if `VOICE_TOOLS_OPENAI_KEY` billing lapses.

**If both break**, Piper is the fully-local, no-key, no-external-dependency fallback (more robotic-sounding):

```yaml
tts:
  provider: "piper"
  piper:
    voice: en_US-lessac-medium
```
Install: `pip install piper-tts` inside the Hermes venv. Models auto-download (~20-90MB) to `~/.hermes/cache/piper-voices/` on first use.

## STT — Groq (current, as of 2026-07-29)

```yaml
stt:
  provider: "groq"
```

Needs `GROQ_API_KEY` in `.env`. Uses `whisper-large-v3`, hosted — offloads compute off this box's 2 vCPU and is noticeably more accurate than the unconfigured default, which is local `faster-whisper` at model `base` (the smallest, least accurate tier). If no `stt:` block is set at all, that weaker local default is what's silently running — always set this block explicitly. Live on both `hermes` and `rishab`/Growify.

Restart after any TTS/STT change: `ssh hermes-root "systemctl restart hermes-gateway.service"` (Dan's own instance) or `ssh hermes-root "systemctl restart hermes-gateway-<client>.service"` (a client instance) — never the bare `hermes gateway restart` alone, since that doesn't specify which unit on a multi-tenant box.

---

## Full skeleton (minimal working config, matches live schema)

```yaml
model:
  provider: anthropic          # or "openrouter" for a client instance — see Model section above
  default: claude-sonnet-5
delegation:
  provider: anthropic
  model: claude-sonnet-5

discord:
  require_mention: true
  free_response_channels: "*"   # remove or scope this if you don't want mention-free chat everywhere

tts:
  provider: "openai"
  openai:
    model: "gpt-4o-mini-tts"
    voice: "alloy"

stt:
  provider: "groq"

repo:
  path: "/path/to/context-2.0"   # wherever Hermes cloned the repo
  remote: "origin"
  branch: "main"
```

`DISCORD_BOT_TOKEN`, `OPENROUTER_API_KEY`, and **`DISCORD_ALLOWED_USERS`** all live in `.env`, not `config.yaml`. Confirmed 2026-07-29: a `discord.allowed_users` list inside `config.yaml` (as shown in earlier drafts of this doc) does **nothing** — the real allowlist gate is the `DISCORD_ALLOWED_USERS` env var, comma-separated user IDs, e.g. `DISCORD_ALLOWED_USERS=123456789012345678,987654321098765432`. Without it set, the gateway logs `No env user allowlists configured` at startup and denies every sender.

---

## SOUL.md — rooting the agent in its actual workspace

`~/.hermes/SOUL.md` is the personality/instruction file — separate from `config.yaml` and separate from the workspace repo's own `CLAUDE.md`. A freshly-provisioned `SOUL.md` is generic boilerplate with **no mention of the workspace at all** — the gateway will run and respond fine, just vaguely, since nothing tells it the repo content exists or matters. Confirmed 2026-07-29 while setting up a second (client) instance — this was the actual cause of "responds fine but vague despite rich context," see `troubleshooting.md`.

Append a second block naming the workspace path and pointing at the repo's own operating-manual file — this is Dan's own, live, working example:

```
Your shared workspace with Dan is /home/hermes/context-2.0-github (repo.path in config.yaml) — the Context 2.0 vault, synced to GitHub, that you both read and write. It is not just a project you have access to; it is the place you and Dan both operate from. The self/ folder within it (self/beliefs.md, self/goals.md, self/arc.md, self/identity.md) holds who Dan is — his identity, active goals, character arc, and beliefs. Read self/goals.md to orient on what's currently active before acting on anything in this workspace. CLAUDE.md at the repo root is the full operating manual — session rhythm, where each kind of update goes, entity schema — treat it as authoritative for how to work in this repo.
```

For a client instance, write the equivalent tailored to that client's actual repo structure (read their real `CLAUDE.md` first, don't assume it mirrors this vault's shape) — full template in `multi-tenant-setup-sop.md` §6. Restart the gateway (`systemctl restart hermes-gateway[-<client>]`) after any `SOUL.md` change for it to take effect.
