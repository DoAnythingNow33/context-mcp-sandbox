# TTS on Discord — Setup Reference

Source: [Hermes Agent docs](https://hermes-agent.nousresearch.com) — TTS feature page, Discord messaging page, and the "Use Voice Mode with Hermes" guide. Fetched 2026-07-08.

Goal: Hermes replies with spoken audio in Discord (DMs / text channels first, voice channels optional/later).

---

## 1. Install the voice extras

On the Hermes machine:

```bash
cd ~/.hermes/hermes-agent && uv pip install -e ".[voice]"
```

Add `".[tts-premium]"` instead/also if using a paid provider (ElevenLabs, OpenAI, etc). `".[all]"` installs everything.

**System dependencies (Ubuntu/Debian — Hermes machine is Linux):**
```bash
sudo apt install portaudio19-dev ffmpeg libopus0 espeak-ng
```
(macOS equivalent: `brew install portaudio ffmpeg opus espeak-ng` — for reference only, not our box.)

---

## 2. `config.yaml` — TTS block

Default provider is **Edge TTS** — free, no API key, good enough to start:

```yaml
tts:
  provider: "edge"
  speed: 1.0
  edge:
    voice: "en-US-AriaNeural"
    speed: 1.0
```

Other providers (elevenlabs, openai, minimax, mistral, gemini, xai, neutts, kittentts, piper) each get their own subsection with provider-specific voice IDs/models — swap `provider:` and add the matching block once we know which one we want. Provider recommendation order from the docs: **Edge (free) → NeuTTS (local) → ElevenLabs (quality) → OpenAI → Mistral (multilingual)**.

Voice recommendation: start with Edge to confirm the pipeline works end-to-end, then upgrade provider once plumbing is verified.

---

## 3. `config.yaml` — Discord voice-related keys

```yaml
discord:
  require_mention: true
  voice_fx:
    enabled: true
    ambient_enabled: true
    ack_enabled: true
```

`voice_fx` only matters for **voice channel** participation (ambient bed + verbal acks), not for TTS replies in text/DMs — safe to leave defaults or disable ambient if it's noisy.

---

## 4. `.env` — credentials

```
# only needed if moving off Edge TTS:
ELEVENLABS_API_KEY=***
VOICE_TOOLS_OPENAI_KEY=***

# STT (voice message transcription) — not required for outbound TTS only:
GROQ_API_KEY=***
```

---

## 5. Discord bot permissions / intents

For **text/DM TTS replies** (no voice channel), the existing bot setup in `config-reference.md` is sufficient — no new permissions needed.

For **Discord voice channel** participation (bot joins a VC and talks), add:

**Bot permissions:** Connect, Speak, Voice Activity (preferred)

**Privileged Gateway Intents (Developer Portal → Bot):** Presence Intent, Server Members Intent, Message Content Intent (the last one should already be on from initial setup).

---

## 6. Turning it on

- Per-message: `/voice tts` — Hermes replies with audio instead of / alongside text.
- `/voice on` — switch a session to always respond with voice.
- `/voice off`, `/voice status` — as expected.
- Discord voice channel only: `/voice join`, `/voice leave`.

Delivery format on Discord: voice bubble (Opus/OGG), falls back to a file attachment if that fails.

---

## 7. Suggested rollout order

1. Confirm text-based Hermes still works normally after installing voice extras.
2. Set `tts.provider: edge` in config.yaml, restart Hermes.
3. In a DM, send `/voice tts` on one message — confirm audio comes back.
4. If good, decide whether to upgrade provider (quality vs. cost) or leave on Edge.
5. Only attempt Discord voice-channel join/leave after step 3 works — separate permission surface, treat as a stretch goal, not day-one requirement.

---

## Troubleshooting

| Symptom | Check |
|---|---|
| "No audio device found" | `portaudio19-dev` not installed — rerun step 1 system deps |
| Bot joins VC but hears/says nothing | Confirm your Discord user ID is in `DISCORD_ALLOWED_USERS`; confirm intents enabled |
| Text works, `/voice tts` produces nothing | Check `tts.provider` config is valid YAML; check `ffmpeg`/`libopus0` installed; check Hermes logs for the TTS provider error |
| Audio comes back garbled/wrong voice | Double check `edge.voice` (or active provider's voice ID) matches a real voice name |
| Works in DM, not in server channel | Same mention-policy issue as text — check `require_mention` / `free_response_channels`, unrelated to TTS itself |

Also see `troubleshooting.md` → "Hermes not responding at all" for base connectivity checks before assuming it's a TTS-specific problem.
