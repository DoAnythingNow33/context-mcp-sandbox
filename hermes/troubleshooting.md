# Hermes Troubleshooting

Diagnostic runbook. Work top-down — most issues are connectivity or config, not model failures.

---

## Hermes is slow to respond

**Step 1 — Identify where the latency is**

Send a trivial message ("ping") and time the response. If it's slow:
- Under 3s: normal
- 3–8s: inference latency, likely model or OpenRouter routing
- 8s+: likely a platform (Discord/Telegram) polling delay or Hermes process issue

**Step 2 — Check OpenRouter status**  
https://openrouter.ai/status — provider outages show here

**Step 3 — Test GLM 5.2 directly**  
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"z-ai/glm-5.2","messages":[{"role":"user","content":"ping"}]}'
```
If this is slow, the issue is upstream (OpenRouter / Z.ai). Switch to fallback model temporarily.

**Step 4 — Check Hermes process**  
```bash
ps aux | grep hermes
# Check memory/CPU — if Hermes process is swapping, restart it
```

---

## Hermes not responding at all

**Discord:**
1. Check bot is online in Discord (green dot on the bot's profile)
2. Check Message Content Intent is enabled in Discord Developer Portal → Bot → Privileged Gateway Intents
3. Check `allowed_users` in config.yaml includes your actual Discord user ID
4. Check Hermes logs for auth errors
5. **Bot online, DMs work, but silent in a server channel:** `require_mention` (default `true`) only gates server/guild channels — DMs are always exempt regardless of this setting. If a channel used to work without `@mention`ing the bot, check `discord.free_response_channels` in config.yaml is set for that channel ID (or `"*"` for "every channel, no mention needed" — safe on a server that's private to just you and the bot). This key is easy to lose during a config migration since it isn't in the minimal skeleton in `config-reference.md`.

---

## Gateway split across root and hermes user

**Symptom:** Config/`.env` edits don't seem to take effect. `hermes update`, `pip install`, or editing anything under the Hermes install fails with permission denied. Or: the bot appears to duplicate replies / drop messages inconsistently.

**Cause:** Hermes Agent has two independent things that can each be owned by a different user: the **install** (`/usr/local/lib/hermes-agent` — source + venv) and the **profile** (`~/.hermes/` — config.yaml, .env, everything else, resolved from whichever user's `$HOME` is running the process). If the install was ever set up as root and later a dedicated non-root user was created (e.g. for Claude Code's `--dangerously-skip-permissions` mode), it's easy for the gateway to keep running as root against `/root/.hermes/` while everyone edits `/home/hermes/.hermes/` believing that's what's live.

**Diagnose:**
```bash
# as root:
hermes config path
# as the intended user:
sudo -u hermes -H hermes config path
```
If these print different paths, you have two separate profiles and the wrong one is live. Also check:
```bash
ps -eo pid,user,ppid,cmd | grep "hermes_cli.main gateway run" | grep -v grep
stat -c "%U:%G %n" /usr/local/lib/hermes-agent
```

**Fix (needs root):**
1. Back up the stale profile before touching anything: `tar czf ~/.hermes-root-backup.tar.gz -C /root .hermes` (tar may warn `file changed as we read it` if the process is still live — that's exit code 1, not fatal, only exit codes >1 mean the archive is actually broken).
2. Stop the wrong-user gateway process.
3. `chown -R <correct-user>:<correct-user> /usr/local/lib/hermes-agent /usr/local/bin/hermes`
4. **Check for a leftover root user-level systemd unit before assuming the process is gone for good:** `hermes gateway install` (without `--system`) creates a *user-level* systemd unit (`~/.config/systemd/user/hermes-gateway.service`, with auto-restart) scoped to whichever user ran the install. If root ran that at some point — separately from, or before, any `--system` install — killing the bare process isn't enough; systemd respawns it. As root: `systemctl --user list-units --all | grep -i hermes`, then `systemctl --user disable --now hermes-gateway`.
5. Reinstall as a proper system service running as the correct user: `sudo hermes gateway install --system --run-as-user <correct-user> --force --start-now --start-on-login`
6. Verify exactly one gateway process is running, owned by the correct user: `ps -eo pid,user,cmd | grep "hermes_cli.main gateway run" | grep -v grep`

Diagnosed and fixed 2026-07-09 — see git history around that date for the full session if this recurs.

**OpenRouter:**
1. Check API key is valid: `echo $OPENROUTER_API_KEY` — should not be empty
2. Check account has credits: https://openrouter.ai/credits

---

## Hermes not reading the repo correctly

```bash
cd /path/to/context-2.0
git status        # should be clean
git log --oneline -5   # check last commits
git pull          # pull any changes from Mac
```

If `git pull` fails or shows conflicts — message Dan immediately with the conflict details, do not auto-resolve.

---

## Multi-tenant gateway install clobbers the wrong unit file

**Symptom:** After running `hermes gateway install --system --run-as-user <newuser>` for a second (client) instance, Dan's own Hermes unit file shows `User=<newuser>` when inspected — even though the running process is unaffected (for now).

**Cause:** The CLI always writes to the fixed path `/etc/systemd/system/hermes-gateway.service` — there's no per-instance naming. A second install overwrites the first instance's unit file in place. Harmless only as long as the original process keeps running (already-running processes aren't restarted by `systemctl start` on an already-active unit) — but the *next* restart/reboot/crash would bring the original instance back up as the wrong user, reading the wrong `$HOME`.

**Fix:** Never run the installer a second time for a different user. Hand-write two separate unit files (see `multi-tenant-setup-sop.md` §7) — one per instance, distinct filenames, each with its own `User=`/`Group=`/`WorkingDirectory=`/env block. `systemctl daemon-reload` after writing both, `enable` both, but only `start` the new one — don't touch the already-running original.

Diagnosed and fixed 2026-07-29 while standing up the Growify (Rishab) instance — see `multi-tenant-setup-sop.md` for the full sequence.

---

## Client gateway throws "No LLM provider configured" or "OPENROUTER_API_KEY not set"

**Symptom:** `journalctl -u hermes-gateway-<client>` shows `RuntimeError: No LLM provider configured` and/or `resolve_provider_client: openrouter requested but OPENROUTER_API_KEY not set`, sometimes alongside a `payment / credit error` warning that looks like a billing problem but isn't.

**Cause:** The `.env` line exists (`OPENROUTER_API_KEY=`) but the value is empty. This typically happens when a secure-paste one-liner using `read -s -p "prompt" VAR` is run in **zsh** — `-p` in zsh's `read` builtin means "read from a coprocess," not "show a prompt," so the prompt never displays and `VAR` silently stays empty. The empty string then gets written to `.env` as if it were real.

**Fix:** Use `printf "prompt"; read -s VAR` instead of `read -s -p`, and always echo `${#VAR}` afterward to confirm a plausible length before trusting it went through. If a paste comes out shorter than expected even with that fix, use `KEY=$(pbpaste)` on the Mac side instead of an interactive terminal paste — one incident saw a 73-character key land as 12 characters via `read -s`, cause undetermined (likely bracketed-paste-mode interaction), fixed instantly by reading the clipboard directly.

Diagnosed and fixed 2026-07-29, same session as the unit-file issue above.

---

## A client instance responds fine but is vague, despite a rich context folder

**Symptom:** Gateway is healthy, no errors in logs, model responds normally — but answers are generic ("I can help with company queries...") instead of pulling specifics from the context repo it has full read access to.

**Cause:** A freshly-provisioned `~/.hermes/SOUL.md` is just the default Nous Research boilerplate — it never mentions the client's repo, never tells the agent to read `CLAUDE.md` first, never states its actual job. The gateway doesn't automatically ground itself in `repo.path`'s content just because the path is configured; `SOUL.md` is what tells it to.

**Fix:** Compare against Dan's own working `~/.hermes/SOUL.md` (has a second paragraph naming the workspace path and pointing at the operating-manual file) and append an equivalent client-specific paragraph — see `multi-tenant-setup-sop.md` §6 for the exact template. Restart the gateway afterward.

Diagnosed and fixed 2026-07-29 on the Growify instance — went from "I can help with company queries" to correctly reading `CLAUDE.md`'s routing table and asking a sharp clarifying question about founder identity, in the same session, purely from the `SOUL.md` change.

---

## OpenRouter 402 errors — two different causes that look similar

**Symptom:** `journalctl` shows `HTTP 402: This request requires more credits, or fewer max_tokens`, with a link to fix it.

**Cause 1 — key-level limit.** The link goes to `openrouter.ai/workspaces/.../keys/<id>` and the message says "adjust the key's weekly/monthly limit." This is the per-key credit cap set when the key was created — only affects that one key.

**Cause 2 — account-level balance.** The link goes to `openrouter.ai/settings/credits` and the message says "add more credits." This is the whole account's real balance — affects **every** key on the account, including Dan's own primary Hermes key, not just the client's.

**Why it can appear out of nowhere:** OpenRouter pre-checks whether the account can afford the *worst case* (`max_tokens × price`) before generating anything, not actual token usage. Switching a client's `model.default` from a cheap model (Gemini Flash) to a pricier one (Claude Haiku 4.5) can trip this even with a generous per-key limit, if the account's real balance is thin — confirmed 2026-07-29, `requested up to 64000 tokens, but can only afford 57859`.

**Fix:** Read which of the two links the error actually gives before doing anything — raising a key's limit does nothing if it's actually cause 2. No gateway restart needed either way; both fixes are live on OpenRouter's side immediately.

Diagnosed and fixed 2026-07-29, same session as the SOUL.md issue above.

---

## Bot replies twice to every message

**Symptom:** Dan's own Hermes bot posts two separate replies to a single Discord message, sometimes with slightly different content (one terse, one more elaborated).

**Cause:** Two separate gateway processes running with the same `DISCORD_BOT_TOKEN` at once — Discord delivers the message to both, and both reply. Confirmed 2026-07-29/30: the canonical instance on the Hetzner box (`hermes-gateway.service`) was running as expected, but a **second, local gateway was also running on Dan's Mac**, launched via a `launchd` agent (`~/Library/LaunchAgents/ai.hermes.gateway.plist`, label `ai.hermes.gateway`) — leftover from local testing before the Hetzner box became the canonical always-on host, quietly surviving reboots/logins ever since.

**Fix:** Don't just `kill` the local process — the `launchd` agent has `KeepAlive` set and relaunches it within seconds under a new PID. Unload the job itself:
```bash
launchctl unload -w ~/Library/LaunchAgents/ai.hermes.gateway.plist
```
Confirm with `launchctl list | grep hermes` (should print nothing) and `ps aux | grep hermes_cli` (should show only the Hetzner-box connection, if checking over SSH — nothing local). The plist file itself was left in place, just unloaded — delete it outright (`rm ~/Library/LaunchAgents/ai.hermes.gateway.plist`) if you want it to never auto-start again, e.g. on next reboot.

**Diagnostic tip:** if a "duplicate reply" bug ever recurs, check for two gateway processes anywhere holding the same token before assuming it's a model/prompt issue — `ps -eo pid,user,cmd | grep "hermes_cli.main gateway run"` on every host that might be running Hermes, not just the canonical server.

---

## Wrong files being updated

Cross-reference Hermes's routing logic against `docs/hermes-capture.md`. The routing table there is the source of truth. If Hermes is filing things incorrectly, update Hermes's system prompt to match the routing rules in that file.

---

## Morning/evening messages not sending

Check the cron schedule inside Hermes's scheduling system (varies by Hermes version — check their docs). Confirm:
- Cron is set for BST (UTC+1 summer, UTC winter) — not UTC flat
- **BST note:** morning = 7:30am BST = 6:30 UTC (summer). Evening = 9pm BST = 8pm UTC. Update cron on 2026-10-25 when clocks go back.
- The repo path in Hermes config matches where the repo is actually cloned

---

## Switching models temporarily (for debugging)

Current live schema is `model:` + `delegation:`, not `inference:` — see `config-reference.md` for the confirmed-live blocks. Both Dan's and Growify's instances run `claude-sonnet-5` for both slots as of 2026-07-29/30 (Dan direct via Anthropic, Growify via OpenRouter). To test a different model temporarily, edit both blocks in `~/.hermes/config.yaml` and restart:
```bash
ssh hermes-root "systemctl restart hermes-gateway.service"                    # Dan's instance
ssh hermes-root "systemctl restart hermes-gateway-<client>.service"           # a client instance
```

---

## Logs

Check Hermes logs first before escalating. Location varies — check Hermes docs or run:
```bash
journalctl -u hermes -n 100 --no-pager   # if running as systemd service
# or
tail -100 ~/.hermes/logs/hermes.log       # if logging to file
```
