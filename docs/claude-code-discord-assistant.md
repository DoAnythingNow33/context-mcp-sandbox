# Claude Code Discord assistant (replacing Hermes' model calls)

Started 2026-10-02. Goal: keep a Discord assistant with Hermes-level context (this vault,
memory, skills, tools, scheduled jobs) **without paying extra usage or API fees**, by
running it as real Claude Code on the Hetzner box so it draws from Dan's Claude Pro plan
limits.

Related: `docs/hermes-cost-efficiency-and-subscription-auth.md` (why Hermes costs money).

## Why

- Hermes is a third-party app. Anthropic bills its OAuth calls against **usage credits /
  extra usage**, not plan limits. Measured 2026-10-02: promo credits "Spent" £0.44 → £0.51
  after a few Hermes Haiku messages, while the plan meter barely moved.
- Interactive Claude Code is first-party and draws from **plan limits** (the usage page
  attributes 100% of plan usage to Claude Code).
- Anthropic's **Channels** feature (research preview) pushes Discord messages into a running
  interactive Claude Code session and lets Claude reply back. Anthropic documents running it
  "in a background process or persistent terminal" for always-on use, so this is a sanctioned
  setup for personal use. Pro accounts without an org need no admin enablement.

## Verified vs not

| Claim | Status |
|---|---|
| Channels + official Discord plugin exist; Pro skips admin enablement; needs Bun | Verified (Anthropic docs) |
| Plugin supports DMs (pairing/allowlist) and opt-in server channels with @mention trigger | Verified (plugin source, ACCESS.md) |
| Plugin relays permission prompts to allowlisted DMs as approve/deny buttons | Verified (plugin source) |
| Plugin server starts on this box and only needs a token | Verified (smoke test) |
| **Channels usage bills plan limits, not credits** | **Not verified** — Anthropic's support article says even third-party apps use plan limits, which contradicts what we measured for Hermes. Only a real test (step 5 below) settles it |
| Ported Hermes skills work unchanged in Claude Code | Not verified — same SKILL.md format, but several mention Hermes-only tools |

## What's already set up (2026-10-02, nothing live, Hermes untouched)

Everything is isolated from the existing `claude` tmux session via a separate config dir.

| Item | Location |
|---|---|
| Bun 1.4.2 (hermes user only, not on PATH) | `/home/hermes/.bun/bin/bun` |
| Assistant Claude Code config dir | `/home/hermes/.claude-assistant/` |
| Discord plugin v0.0.4 + deps installed | `~/.claude-assistant/plugins/cache/claude-plugins-official/discord/0.0.4/` |
| Permissions (allow read/search/git; deny sudo, systemctl, `rm -rf`, secret files) | `~/.claude-assistant/settings.json` |
| Persona + memory ported from Hermes SOUL.md / USER.md / MEMORY.md | `~/.claude-assistant/CLAUDE.md` |
| Dan's 8 custom Hermes skills (copies) | `~/.claude-assistant/skills/` |
| Launcher (tmux session `assistant`, auto-restart loop, refuses to start without login + token) | `/home/hermes/claude-assistant/start-assistant.sh` |
| systemd unit — **not installed** | `/home/hermes/claude-assistant/claude-assistant.service` |
| crontab for vault pulls — **not installed** | `/home/hermes/claude-assistant/crontab.proposed` |

Ported skills: external-comms-approval-gate, token-sniper-bot, composio, composio-cli,
composio-integration, agent-tool-usage-best-practices, shared-git-vault-sync,
date-time-awareness. The other ~73 Hermes skills are bundled defaults (many macOS-only) and
were not ported.

### Permission mode — important

The repo's `.claude/settings.local.json` sets `defaultMode: bypassPermissions`, which every
Claude Code session started in this repo inherits. On 2026-10-03 Dan chose to run the
assistant with `--dangerously-skip-permissions` too, so it never asks before acting: anyone
who can message the bot effectively has a shell as the `hermes` user. Keep the access policy
on `allowlist` with only Dan paired, and don't add server channels other people post in.
To go back to approve/deny buttons in Discord DMs, change the launcher flag to
`--permission-mode acceptEdits`.

## Steps only Dan can do

All commands as root on the box unless noted.

1. **Create a new Discord bot** (do not reuse the Hermes bot token, or both will answer —
   the double-reply problem from runbook §5). Developer Portal → New Application → Bot →
   Reset Token, copy it. Turn **Public Bot off**. Enable **Message Content Intent**. OAuth2 →
   URL Generator → scope `bot`, permissions: View Channels, Send Messages, Send Messages in
   Threads, Read Message History, Attach Files, Add Reactions. Invite it to your server.

2. **Log in and add the token** (one-time, interactive):
   ```bash
   su - hermes
   export CLAUDE_CONFIG_DIR=~/.claude-assistant PATH=~/.bun/bin:$PATH
   cd ~/context-2.0-github && claude
   ```
   In Claude Code: `/login` (Dan's Pro account, dan.cktk@gmail.com), then
   `/discord:configure <bot token>`, then `/exit`.

3. **Start it:**
   ```bash
   ~/claude-assistant/start-assistant.sh      # still as hermes
   tmux attach -t assistant                   # Ctrl-b d to detach
   ```
   The startup screen should show the channels notice for `plugin:discord@claude-plugins-official`.

4. **Pair and lock down.** DM the new bot from Discord; it replies with a code. In the
   attached session: `/discord:access pair <code>`, then `/discord:access policy allowlist`.
   Optional server channel: `/discord:access group add <channel id>` (mention-only by default).

5. **Billing test — before relying on it.** Note claude.ai → Settings → Usage: the credits
   "Spent" line and the plan %. Send the bot ~10 real messages. Re-check:
   - credits unchanged, plan % up → works as intended, continue;
   - credits went up → Channels are billed like Hermes; stop and rethink.

## Cutover (after step 5 passes)

1. Stop the Hermes gateway (keep it installed for rollback):
   `systemctl stop hermes-gateway.service && systemctl disable hermes-gateway.service`
2. Move the vault pulls off Hermes: install `crontab.proposed` (instructions inside it).
3. Run on boot: install `claude-assistant.service` (instructions inside it).

**Rollback:** `tmux kill-session -t assistant` (as hermes), then
`systemctl enable --now hermes-gateway.service`.

## What you lose vs Hermes

- Voice in/out (Hermes used OpenAI TTS + Groq STT). The assistant replies in text.
- Hermes' background skill/memory curation. Claude Code has its own auto memory instead.
- Separate conversations per channel: it's one long session, auto-compacted, handling
  messages one at a time.
- Cron delivery to Discord: the proposed crontab logs to
  `/home/hermes/claude-assistant/vault-autopull.log` instead of the Hermes log channel.

## Risks

- **Shared limits.** The assistant uses the same 5-hour and weekly Pro limits as Dan's own
  Claude Code work. When they run out, it stops.
- **Usage credits.** If "usage credits" are turned on in claude.ai usage settings, Claude
  Code past a plan limit spends them. Turning them off guarantees no extra cost but also
  breaks Hermes (which bills credits) — only do that after cutover.
- **Research preview.** `--channels` syntax/behaviour may change; the flag isn't listed in
  `claude --help`.
- **Fragility.** One process; the launcher's loop restarts it on exit, but a hung session
  needs `tmux attach -t assistant` to fix.

## Known issue found while setting this up (FIXED 2026-10-07)

> Fixed: work committed + pushed, and `vault-autopull.sh` now rebases with autostash and only alerts on conflict. Root cause was a dirty tree plus a diverged branch (weekly self-heal Action pushes to GitHub). Original note follows.


The Hermes "Vault Auto-Pull" cron jobs have been **skipping** since at least 2026-10-01 22:00
with "working tree has uncommitted changes". Uncommitted on 2026-10-02: `index.md`,
`docs/hermes-cost-efficiency-and-subscription-auth.md`, `docs/ARCHITECTURE-JEV-ROUTING.md`,
`entities/projects/context-mcp/`, plus this file. Commit or stash them to get pulls going again.

## Incident: assistant offline 2026-10-05 → 2026-10-07 (OOM kill)

**Symptom:** Discord bot stopped answering. No `assistant` tmux session, no `claude --channels`
process.

**Cause:** Kernel OOM killer. The box has 3.8 GB RAM and **no swap**. On 2026-10-05 ~10:24–10:29
the assistant ran a `faster-whisper` **medium** model test (`~/voice/stt.py ... medium`, exit
code 137). The OOM killer reaped processes in the `tmux-spawn-*` scope, which took down the
assistant's tmux session, including the restart loop in `start-assistant.sh` (the loop lives
inside tmux, so it can't survive its own session being killed). `claude-assistant.service` was
never installed, so nothing relaunched it.

**How it was diagnosed (repeatable):**
1. `ps aux | grep claude` and `tmux ls` as hermes: no `assistant` session.
2. Last line of the newest `~/.claude-assistant/projects/*/*.jsonl`: tool_result `Exit code 137`.
3. `journalctl -k | grep -iE 'oom|killed process'`: OOM entries at the same timestamps.
4. `.credentials.json` `expiresAt` was also past (Oct 5 12:08) but the token refreshes itself;
   after restart the session showed "Claude Pro" with no re-login needed.

**Recovery (done 2026-10-07 08:20):**
```bash
sudo -u hermes -H bash -c '~/claude-assistant/start-assistant.sh'
sudo -u hermes tmux capture-pane -t assistant -p      # check it's logged in
ps -u hermes -o pid,args | grep -E 'channels|bun'     # plugin server running
```

**Hardening (done 2026-10-07 by Dan + Claude):**
- 4 GB `/swapfile` (in `/etc/fstab`), `vm.swappiness=10`.
- `claude-assistant.service` installed in `/etc/systemd/system/` and enabled. It is now
  `Type=simple`, `Restart=always`, `RestartSec=15`, `OOMScoreAdjust=-500`, running
  `~/claude-assistant/run-assistant.sh`: it calls `start-assistant.sh`, then stays alive while
  tmux session `assistant` exists and exits non-zero when it disappears, so systemd restarts it.
  The unit source is `~/claude-assistant/claude-assistant.service` (copy to /etc/systemd/system,
  `daemon-reload`, `restart`).
- Tested: `tmux kill-session -t assistant` as hermes, and the service recreated it.
- Check: `systemctl status claude-assistant`, `tmux ls` (as hermes).

**Rules to avoid a repeat:**
- Don't run Whisper `medium` (or other multi-GB jobs) on this box; use `small`/`base`.
  Voice STT in `~/voice/stt.py` was edited to take a model arg; default is `small`.
- Until swap is added, a second memory-heavy process next to the Hermes gateways (2),
  the `claude` tmux session and the assistant can trigger this again.
- Check for this fast: `tmux ls` as hermes shows `assistant`; `journalctl -k | grep -i oom`.
