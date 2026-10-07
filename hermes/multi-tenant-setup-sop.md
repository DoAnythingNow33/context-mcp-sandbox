# SOP — Standing Up a New Client Hermes Instance

Generic template for onboarding a client onto Dan's own Hetzner box as a colocated, isolated Hermes instance — one Linux user, one Discord bot, one context repo, one billing key per client. First run was Growify/Rishab, 2026-07-28 → 2026-07-29 (see "Worked example" at the bottom for the exact commands used). Every pitfall hit during that first run is folded into the steps below — this is the corrected version, not the naive one.

Placeholders used throughout: `<client>` (short slug, e.g. `growify`), `<user>` (Linux username, e.g. `rishab` — usually the primary contact's first name, not the company name), `<account>` (Dan's GitHub account).

**Do not run these steps unattended.** Every step touches Dan's live production Hermes server (also runs Dan's own always-on assistant). Run interactively, one section at a time, and re-verify Dan's own Hermes is still healthy after each step that touches shared services (systemd, package installs).

---

## 0. Pre-flight — decisions to confirm before starting

| Decision | Recommended default | Why it matters |
|---|---|---|
| Linux username | Client contact's first name (e.g. `rishab`), not the company | Mirrors the `hermes` user pattern (`infrastructure.md`); one user per human contact, not per company, since a company may later add a second founder as a second contact sharing the same context repo |
| Context folder repo | New private GitHub repo, `<client>-context`, owned under Dan's GitHub | Client isn't necessarily technical; keeps Dan as sync operator |
| Billing for the client's model usage | Separate OpenRouter API key, credit-limit capped, monthly reset | Keeps usage attributable and billable; **does not fully isolate cost** — see §5, the cap only limits that key's own spend, but a low *account balance* still blocks every key sharing the account |
| Discord bot/server | New Discord application per client, new (or client's own) server, client's Discord ID(s) allowlisted | Keep separate from Dan's own personal Hermes Discord presence |
| Airtable/other live-data integration | Manual export → folder first; live pull script as a later phase | Filter manually before automating — avoids importing noise along with signal |

If any of these should be different for a given client, adjust the steps below before running them.

---

## 1. Resource check first

The box is small: 2 vCPU, 3.7GB RAM (`infrastructure.md`). Before adding another always-on gateway process, confirm there's headroom:

```bash
ssh hermes
free -h
ps -eo pid,user,%mem,%cpu,cmd | grep hermes_cli | grep -v grep
```

If existing gateways are already using a meaningful chunk of the 3.7GB, another full gateway may cause swapping. If tight, the fallback is a bigger Hetzner plan (cheap to upgrade) — flag to Dan, don't just proceed. Each gateway process has run at roughly 100–200MB RSS in practice (confirmed with two concurrent instances, 2026-07-29) — a handful of clients should fit comfortably before this box needs upgrading.

---

## 2. Create the new Linux user

```bash
ssh hermes-root "adduser <user> --disabled-password --gecos ''"
```

(Dan's own `hermes` user has no sudo — admin actions need the separate `hermes-root` SSH alias, `User root` in `~/.ssh/config`. Check `~/.ssh/config` for this before assuming you need a password prompt.)

Give it SSH access via Dan's own admin key (not the client's), plus a local alias:

```bash
ssh hermes-root "
mkdir -p /home/<user>/.ssh
cp /root/.ssh/authorized_keys /home/<user>/.ssh/authorized_keys
chown -R <user>:<user> /home/<user>/.ssh
chmod 700 /home/<user>/.ssh && chmod 600 /home/<user>/.ssh/authorized_keys
"
```

Add to Dan's local `~/.ssh/config`:

```
Host <client>-hermes
    HostName 5.75.188.204
    User <user>
    IdentityFile ~/.ssh/id_ed25519
```

Verify: `ssh <client>-hermes whoami` should print `<user>`.

---

## 3. Reuse the existing Hermes install, give it its own profile

The Hermes Agent binary/venv at `/usr/local/lib/hermes-agent` is shared — no reinstall needed. What's per-user is the **profile** (`~/.hermes/` — config, secrets, state), resolved from whichever user's `$HOME` runs the process.

```bash
ssh <client>-hermes "hermes config path"
# must print /home/<user>/.hermes/config.yaml — NOT /root/.hermes or another user's home
```

If it doesn't resolve there, don't proceed — see `troubleshooting.md` → "Gateway split across root and hermes user" for the diagnosis pattern (same root cause applies to any user, not just `hermes`).

---

## 4. Config — `/home/<user>/.hermes/config.yaml`

**Always read Dan's own live config first and match its actual schema** — don't trust any config snippet in this repo's docs without cross-checking, including this one:

```bash
ssh hermes "cat ~/.hermes/config.yaml"
```

Schema confirmed live as of 2026-07-29:

```yaml
model:
  provider: openrouter
  default: google/gemini-2.5-flash    # or anthropic/claude-haiku-4.5 — see model choice note below
delegation:
  provider: openrouter
  model: anthropic/claude-sonnet-5

discord:
  require_mention: true
  free_response_channels: "*"

repo:
  path: /home/<user>/<client>-context
  remote: origin
  branch: main
```

**Model choice note:** `model.default` is the conversational model (cheap, high-volume); `delegation.model` is what actually executes tool-use/task work (pricier, lower-volume). Gemini Flash is the cheapest conversational option; Claude Haiku 4.5 costs more per token but may be worth it for response quality — if switching, see §5's credit-limit gotcha before assuming it'll "just work."

**Secrets go in `.env`, never `config.yaml`:** `DISCORD_BOT_TOKEN`, `OPENROUTER_API_KEY`, and **`DISCORD_ALLOWED_USERS`** (comma-separated Discord user IDs — confirmed 2026-07-29 this is the *actual* allowlist gate; a `discord.allowed_users` key inside `config.yaml` does nothing at all, silently). Without `DISCORD_ALLOWED_USERS` set, the gateway logs `No env user allowlists configured` at startup and denies every sender.

**Pasting secrets without exposing them in chat or shell history:**

```bash
printf "Paste the key: "; read -s KEY; echo
printf '%s' "$KEY" | ssh <client>-hermes '
  KEY=$(cat)
  grep -v "^SOME_VAR=" ~/.hermes/.env > ~/.hermes/.env.tmp 2>/dev/null || touch ~/.hermes/.env.tmp
  echo "SOME_VAR=$KEY" >> ~/.hermes/.env.tmp
  mv ~/.hermes/.env.tmp ~/.hermes/.env
  chmod 600 ~/.hermes/.env
  echo "wrote SOME_VAR (${#KEY} chars)"
'; unset KEY
```

Do **not** use `read -s -p "prompt" VAR` — in zsh, `-p` means "read from a coprocess," not "show a prompt," and silently leaves `VAR` empty (which then gets happily written to `.env` as an empty value, producing a confusing "not set" error later). The `printf` + bare `read -s` form above works in both bash and zsh.

Always check the char-count echo before trusting a paste went through. If it comes out shorter than expected even with the correct syntax (happened once — a 73-character key landed as 12 via `read -s`, likely a bracketed-paste-mode interaction), use `KEY=$(pbpaste)` on the Mac side instead of an interactive terminal paste.

---

## 5. Billing — OpenRouter key setup, and the credit-limit trap

Create a separate key per client at `openrouter.ai/keys` → name it (e.g. `<Client>-Agent`) → set a **credit limit** (recommend $30–50 to start) with **monthly** reset.

**Two different failure modes look almost identical but need different fixes — check which one you're hitting:**

1. **Key-level limit hit.** Error mentions "adjust the key's weekly/monthly limit" and links to the key's own settings page (`openrouter.ai/workspaces/.../keys/...`). Fix: raise or clear that specific key's limit.
2. **Account-level balance too low.** Error mentions "add more credits" and links to `openrouter.ai/settings/credits`. This is **account-wide** — it affects every key on the account, including Dan's own primary Hermes key, not just the client's. Fix: top up real credits on the account.

Why this bites specifically when switching to a pricier model (e.g. Gemini Flash → Claude Haiku 4.5): OpenRouter pre-checks that the account can afford the **worst case** (`max_tokens × price`) before generating anything at all, not actual usage. A request that was previously fine under a cheap model can fail under a pricier one purely on this pre-check, even with a generous per-key limit, if the account's real balance is thin. Confirmed 2026-07-29: switching Rishab's instance to Haiku produced `HTTP 402: requested up to 64000 tokens, but can only afford 57859` — first diagnosed as a key-limit issue (it wasn't, that was already unlimited), actually an account balance issue.

No gateway restart is needed after topping up credits or raising a key limit — both are live on OpenRouter's side, not local config.

---

## 6. Root the assistant in the client's context folder (`SOUL.md`)

**This step is easy to skip and produces a working-but-useless assistant if you do.** A freshly-provisioned `~/.hermes/SOUL.md` is generic boilerplate ("You are Hermes Agent, an intelligent AI assistant created by Nous Research...") with zero mention of the client's folder. The gateway will run fine, respond fine, and be completely vague — it doesn't know to read the context repo unless told to. Confirmed 2026-07-29: this was the actual cause of "vague answers despite rich context available," not a model or config problem.

Compare against Dan's own working `~/.hermes/SOUL.md` — it has a second paragraph naming the workspace path, pointing at `self/goals.md` for orientation and `CLAUDE.md` as the operating manual. Write the equivalent for the client, tailored to whatever routing structure their actual repo uses (read the client repo's own `CLAUDE.md` first — don't assume it matches Dan's own vault's shape):

```bash
ssh <client>-hermes "cat >> ~/.hermes/SOUL.md << 'EOF'


You are the <Client> Assistant — <contact>'s always-on AI assistant for <Client>. Your shared workspace with <contact> is /home/<user>/<client>-context (repo.path in config.yaml), synced to GitHub. This is not a generic project you happen to have access to; it is the single source of truth for <Client> that you and <contact> both read from and write to.

Read CLAUDE.md at the repo root first, every session — it is the map. [Add repo-specific routing detail here — read the actual CLAUDE.md and summarise its structure/anchor-principle/routing-table, don't guess.] Then go to the specific entity file the question is actually about rather than answering from a summary alone if more detail exists.

Your job right now is specifically: help <contact> push new context into this folder (voice notes, quick updates, corrections) and pull existing context back out (answer questions, surface what's already known) — grounded in what's actually written in these files, not generic advice. If something isn't in the folder yet, say so plainly and offer to capture it, rather than answering vaguely or generically. [Note any not-yet-built integrations here, e.g. MCP connections to other client tools, so the assistant doesn't imply capabilities it doesn't have.]
EOF
"
```

Restart the gateway afterward for it to take effect (§8 covers restart commands).

---

## 7. Airtable / other live-data connections

Keep this simple on day one and upgrade later:

**Phase 1:** client exports their data (CSV or native export). Dan manually converts it into the context repo's folder structure, matching whatever entity pattern the repo already uses. No live API involved yet.

**Phase 2 (a later phase, not day one):** a small per-client Python script using the client's own API token (their `.env`, read-only scope to start) to pull records on a schedule and write/update the corresponding markdown files — same shape as `generate_digest.py` regenerating `_digest.md` from snapshot files in Dan's own vault.

---

## 8. New Discord bot

1. discord.com/developers/applications → New Application → name it client-facing, e.g. "`<Client>` Assistant"
2. Bot tab → Add Bot → Reset Token → copy it → written into `.env` as `DISCORD_BOT_TOKEN` (§4's secure-paste pattern)
3. Bot tab → Privileged Gateway Intents → enable **Message Content Intent**
4. **Bot Permissions checklist** (same tab, further down): leave all of **General Permissions** unchecked (no Administrator, no Manage Server, etc.); under **Text Permissions** check only `Send Messages` + `Read Message History`; leave Voice Permissions and everything else unchecked
5. If Bot tab → **Public Bot** is off (recommended for a single-client bot), also go to the **Installation** tab and set **Default Authorization Link** to **None** — otherwise the OAuth2 URL Generator throws a validation error ("Private application cannot have a default authorisation link")
6. OAuth2 tab → URL Generator → scope `bot` → the same two permissions from step 4 → copy the generated URL → open it → pick the server → authorize
7. Client enables Developer Mode (Settings → Advanced) → right-clicks their own username → Copy User ID → goes into `DISCORD_ALLOWED_USERS` in `.env` (§4) — add Dan's own Discord ID here too, temporarily, so Dan can test before the client does
8. If a bot token is ever pasted into a chat/log in plaintext (rather than piped via the secure paste pattern), reset it once everything's verified working — cheap insurance, no downside

---

## 9. Gateway service — install as a distinct systemd unit

**Never run `hermes gateway install --system --run-as-user <user>`.** Confirmed 2026-07-29: the CLI always writes to the same fixed path, `/etc/systemd/system/hermes-gateway.service` — there is no per-instance naming flag. Running it a second time **overwrites whatever instance's unit file already exists there** (survived the first time only because the already-running process pre-dated the file being overwritten and wasn't restarted — the next reboot or crash would have brought the original instance back up as the wrong user, reading the wrong `$HOME`). Hand-write separate unit files instead, always.

**First, read the existing unit file in full** (not just `User=`/`ExecStart=`) so you can reconstruct anything if it goes wrong:

```bash
ssh hermes-root "cat /etc/systemd/system/hermes-gateway.service"
```

Write a new file `/etc/systemd/system/hermes-gateway-<client>.service` — identical shape, with `User=<user>`, `Group=<user>`, `WorkingDirectory=/home/<user>/.hermes`, and `HOME`/`USER`/`LOGNAME`/`HERMES_HOME`/`PATH` env lines all pointed at `/home/<user>`. Give it a distinct `Description=`. **Do not touch the existing file for any other instance.**

```bash
ssh hermes-root "systemctl daemon-reload && systemctl enable hermes-gateway-<client>.service && systemctl start hermes-gateway-<client>.service"
```

Verify one process per instance, each owned by the correct user:

```bash
ssh hermes-root 'ps -eo pid,user,cmd | grep "hermes_cli.main gateway run" | grep -v grep'
```

To restart a single client's instance after a config/`.env`/`SOUL.md` change: `ssh hermes-root "systemctl restart hermes-gateway-<client>.service"` — never `restart` without the client suffix, and never touch another instance's unit while doing so.

If a gateway throws `RuntimeError: No LLM provider configured` or `openrouter requested but OPENROUTER_API_KEY not set` in `journalctl -u hermes-gateway-<client>`, check the key actually has content first (§4's char-count check) before assuming it's a billing issue — an empty-but-present `OPENROUTER_API_KEY=` line produces exactly this error.

---

## 10. Repo — get the client's context folder onto GitHub, then clone it to the server

Check first whether a real context folder already exists locally (e.g. a client vault built via the `client-vault` skill, possibly Google-Drive-synced) before assuming an empty repo needs seeding.

**If a local folder already exists with no GitHub remote yet:**

```bash
cd "/path/to/local/vault"
git init -q
echo ".DS_Store" > .gitignore
git add -A
git commit -q -m "Initial import"
git branch -M main
git remote add origin https://github.com/<account>/<client>-context.git
git push -u origin main --force   # --force only if a placeholder repo was already created and needs replacing
```

If the folder is Google-Drive-synced, Drive will now sync the `.git` internals too — can occasionally cause file-lock conflicts mid-commit. Fine for occasional commits; move the repo out of Drive entirely if commit frequency picks up.

**On the server, use a dedicated per-client SSH deploy key** — don't reuse Dan's personal GitHub key for a client repo:

```bash
ssh <client>-hermes "ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_<client> -N '' -C '<user>@<client>-hermes deploy key' -q && cat ~/.ssh/id_ed25519_<client>.pub"
# copy the printed public key, then, from Dan's Mac:
gh repo deploy-key add /dev/stdin --repo <account>/<client>-context --title "<client>-hermes deploy key" --allow-write <<< "<paste public key>"
```

Wire up a dedicated SSH host alias so git uses that key specifically:

```bash
ssh <client>-hermes "
cat >> ~/.ssh/config << 'EOF'

Host github.com-<client>
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_<client>
    IdentitiesOnly yes
EOF
chmod 600 ~/.ssh/config
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts
git clone git@github.com-<client>:<account>/<client>-context.git ~/<client>-context
"
```

Confirm `git status` is clean and `CLAUDE.md` at the repo root is real content, not a placeholder. **If local content was pushed with `--force` after the server already had a clone from an earlier, different history, delete and re-clone rather than `git pull`** — a force-push replaces history entirely, so the old clone shares no common ancestor to merge from.

If the local vault's own `CLAUDE.md` has a stale "not a git repo" note (common if it started as a Drive-only vault before this SOP ran), update it once the repo is live — an agent reading it will otherwise think there's no revert safety net when there now is one.

---

## 11. Verify end-to-end

1. `systemctl status hermes-gateway-<client> --no-pager` — active, correct PID, correct user
2. `journalctl -u hermes-gateway-<client> -n 20` — no `RuntimeError: No LLM provider configured`, no `allowlists configured` warning
3. Message the bot from Dan's own (temporarily allowlisted) Discord account first — confirm a real, *specific* reply grounded in the actual context repo content, not generic assistant boilerplate (if it's vague, go back to §6 — this is the single most common miss)
4. Then have the actual client message it
5. Confirm Dan's **own** Hermes is still responding normally — sanity check nothing on the shared box got disturbed
6. `free -h` again — confirm no swap pressure with all gateways live

---

## 12. Explicitly out of scope for a first pass

- Live third-party data sync (Airtable/etc.) — manual export/import only until Phase 2
- Additional contacts at the same client (e.g. a co-founder) sharing the same context repo — add as a second Discord ID in the same `.env`'s `DISCORD_ALLOWED_USERS`, not a second Linux user, unless they need genuinely separate access control
- Voice/TTS — a separate pass, not a day-one requirement (see `tts-discord-setup.md` for Dan's own setup if a client wants this later)
- Write-access from the assistant back into any third-party tool — read-only to start

---

## Worked example — Growify / Rishab (2026-07-28 → 2026-07-29)

- `<user>` = `rishab`, `<client>` = `growify`, SSH alias `growify-hermes`
- Context repo: existing Google-Drive-synced local vault at `~/Library/CloudStorage/GoogleDrive-.../Shared drives/Growify x DAN./vault` (250+ files, real founder/ontology content, not a fresh build) → pushed to new private repo `<account>/growify-context`
- Model: started on `google/gemini-2.5-flash`, switched to `anthropic/claude-haiku-4.5` mid-session per Dan's request (triggered the account-balance credit issue in §5), then collapsed to `anthropic/claude-sonnet-5` for both slots on 2026-07-29 to match Dan's own single-model setup
- Discord app: "Growify Assistant" — bot token pasted in plaintext once by mistake, reset immediately as a precaution
- Full detail of what went wrong and got fixed live: `troubleshooting.md` → "Multi-tenant gateway install clobbers the wrong unit file", "Client gateway throws 'No LLM provider configured'...", and the OpenRouter/credit entries
- Status snapshot: `actions/backlog/growify-dan-hermes-setup.md`
