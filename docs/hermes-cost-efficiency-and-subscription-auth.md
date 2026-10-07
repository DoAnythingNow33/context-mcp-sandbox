# Hermes: cost efficiency + subscription auth runbook

Written 2026-09-30 after diagnosing a $4.78 / 6.6-minute cost spike and a client-visible
outage on the Growify (rishab) Hermes instance. Use this when: a client reports a Hermes
provider failure, a bill looks too high for what was asked, or you're onboarding a new
client instance.

## 1. What actually happened (Growify incident, 2026-09-27)

Symptom: client saw `⚠️ The model provider failed after retries` twice in Discord after
asking for a small config fix.

Root cause, confirmed from `journalctl -u hermes-gateway-<instance>.service` and the
OpenRouter activity export:

- Hermes fires an automatic **background review** pass after every N turns
  (`skills.creation_nudge_interval` / `memory.nudge_interval`, default **10**) that
  replays the conversation through the *live* model to update the skill/memory library.
  This runs in a background thread, concurrently with the reply the user is waiting on.
- By default this background pass uses the **same model as the parent conversation**
  (Sonnet 5 in this case) and, worse, **replays the growing tool-call history on every
  iteration of its own tool loop** — 30 sequential API calls in this incident, prompt
  tokens climbing from 29K to 201K while `tokens_cached` stayed flat (~29K). That means
  ~170K tokens of context were resent, uncached, on nearly every one of those 30 calls.
  Total cost for that one triggered review: **$4.78 across 32 calls in 6.6 minutes**
  (verified against the OpenRouter CSV, `cost_total` column, session `20260927_160058`).
- Because the background thread and the live reply thread were in flight on the OpenRouter
  account at the same time, OpenRouter returned `HTTP 402 in_flight_budget_exhausted`
  (not a generic outage — check the actual error body, not just the gateway's user-facing
  message). No `fallback_model` was configured, so the failure surfaced raw to the client
  instead of failing over.

**Diagnostic pattern to look for next time:** in the OpenRouter/Anthropic usage export,
a burst of many rows within a few minutes, same session, `tokens_prompt` climbing steadily
while `tokens_cached` stays flat — that's an uncached background tool-loop, not a single
expensive prompt.

## 2. The fix (apply to every instance)

Add to `~/.hermes/config.yaml` for the Hermes OS user running the instance:

```yaml
auxiliary:
  background_review:
    provider: anthropic        # or openrouter — match how the instance is billed
    model: claude-haiku-4.5    # or anthropic/claude-haiku-4.5 for openrouter
fallback_model:
  provider: openrouter         # safety net if primary auth/credit/rate-limit fails
  model: anthropic/claude-sonnet-4
```

Why this works:
- Pointing `background_review` at a **different model** than the parent conversation
  switches Hermes from full-transcript replay to a **compact digest** internally
  (`agent/background_review.py::_resolve_review_runtime` — same model = full replay,
  different model = digest). This alone removes the quadratic-cost tool-loop problem,
  independent of which model you pick.
- Haiku is also ~10-20x cheaper per token than Sonnet, so even the digest calls cost
  a fraction of a cent.
- `fallback_model` makes 402 (billing/credits), 429 (rate limit), 503/529 (overload) fail
  over automatically instead of showing the user a raw error. Confirmed in
  `agent/conversation_loop.py` — `FailoverReason.billing` (which 402 maps to) is one of
  the eager-fallback triggers.

Optional second lever: raise `skills.creation_nudge_interval` / `memory.nudge_interval`
(default 10) if background reviews still fire too often for the client's usage pattern.
Do the cheap-model fix first — it's a bigger win with less impact on the skill/memory
library staying fresh.

### Gotcha: file ownership

Each Hermes instance runs as its own OS user (`hermes`, `rishab`, future clients get their
own). If you edit `config.yaml` as `root`, **it becomes root-owned and the service user can
no longer read its own config** — Hermes silently falls back to defaults (or crash-loops
with `Permission denied` in the journal). Always run immediately after editing as root:

```bash
chown <service_user>:<service_user> ~<service_user>/.hermes/config.yaml
chmod 600 ~<service_user>/.hermes/config.yaml
```

### Applying + verifying

```bash
systemctl reload hermes-gateway-<instance>.service
# Expect one self-restart (exit code 75/TEMPFAIL) — this is normal, Hermes exits itself
# to pick up new config and systemd (RestartForceExitStatus=75) brings it back.
sleep 10
systemctl show hermes-gateway-<instance>.service -p NRestarts,ActiveState,SubState
journalctl -u hermes-gateway-<instance>.service --since "-30s" | grep -i "permission\|error\|config"
```
Confirm `ActiveState=active`, `SubState=running`, no config/permission errors, and the
restart counter stops climbing.

## 3. Running an instance on a Claude subscription instead of metered billing

Metered API billing (OpenRouter or direct `ANTHROPIC_API_KEY`) charges per token with no
ceiling. Hermes can instead authenticate with a Claude login (`model.provider: anthropic`
plus a Claude Code OAuth credential) — but **this is not a flat-rate plan.** Anthropic bills
third-party apps (Hermes counts as one) against the account's **extra usage / usage
credits**, not its plan limits. Verified 2026-10-02: after Hermes messages the plan meter
barely moved while promo credits dropped (£0.44 → £0.51 over a few Haiku messages), and an
org with extra usage off gets rejected outright (see "Extra usage requirement" below).
What you gain over an API key is a capped, visible spend (the monthly spend limit on the
usage page), not a flat fee.

**Credential resolution — what actually decides.** The old single-token resolver
(`agent/anthropic_adapter.py::resolve_anthropic_token`) lists OAuth before the API key, but
the running agent builds a credential *pool* (`agent/credential_pool.py`,
`_seed_from_singletons`). If `ANTHROPIC_API_KEY` is set in `~/.hermes/.env` and no
`ANTHROPIC_TOKEN` / `CLAUDE_CODE_OAUTH_TOKEN` is set, Hermes treats that as "the user chose
the API-key path" and **refuses to seed the Claude Code OAuth login into the pool.** The
instance then bills the metered key even though a valid `~/.claude/.credentials.json`
exists. (Found 2026-10-02 on the personal `hermes` instance: $0.13 of API charges for
Haiku calls despite a working OAuth login.)

So: **to use a Claude login, remove `ANTHROPIC_API_KEY` from `~/.hermes/.env`** (keep a
`.env.bak-*` copy). Do not rely on it being "just a fallback".

### Extra usage requirement

On Claude Team (and any account without extra usage enabled), Hermes calls fail with:
`HTTP 400: Third-party apps now draw from your extra usage, not your plan limits.`
The login's own profile shows it — `~/.claude.json` → `oauthAccount.hasExtraUsageEnabled`
(`True` on the working personal Pro account, `False` on the Growify Team org). Fix: the org
owner enables extra usage and sets a spend cap at claude.ai/admin-settings/usage. This is
independent of model — Haiku is refused as well as Sonnet.

### Setup steps (per instance)

1. `config.yaml`: set `model.provider: anthropic` (and `delegation.provider: anthropic`,
   `auxiliary.background_review.provider: anthropic` if using the fix above).
   Remove `ANTHROPIC_API_KEY` from `~/.hermes/.env` (see above) and enable extra usage on
   the Claude account.
2. As the instance's OS user, authenticate:
   ```bash
   su - <service_user>
   claude /login          # or: claude setup-token
   ```
   This writes `~/.claude/.credentials.json` tied to whatever Claude.ai account/subscription
   is logged into in that shell.
3. Reload the gateway service (see §2) and verify — see below.
4. Keep `fallback_model` pointed at metered OpenRouter/API billing. Subscriptions have
   rolling usage caps (like Claude Code's 5-hour windows); a burst of tool calls can trip
   them. Without a fallback, that becomes a client-visible outage instead of a cost line
   item — same failure mode as the original incident, just capped by time instead of
   dollars.

### Verifying it's actually using the Claude login, not the API key

1. List the pool as the service user:
   ```bash
   sudo -u <service_user> env HERMES_HOME=/home/<service_user>/.hermes \
     /usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main auth list anthropic
   ```
   Expect exactly one credential: `claude_code  oauth`. If an `env:ANTHROPIC_API_KEY` entry
   remains after reload, remove it: `... auth remove anthropic <index>`.
2. Send a real message and check `~/.hermes/logs/agent.log` for `provider=anthropic` and no
   `Fallback to openrouter` line.
3. Check claude.ai → Settings → Usage: the credits "Spent" figure should rise by a cent or
   two per message, and the API console should show no new charge.

**The old PONG test (`env -u ANTHROPIC_API_KEY ... -z PONG`) does not prove OAuth.** Hermes
reads `~/.hermes/.env` itself and prefers it over the process environment, so stripping the
shell variable changes nothing. It passed on 2026-09-30 while the instance was still
billing the API key.

## 4. Per-client policy — do not share your personal subscription

**Never point a client's production/commercial bot at your own personal Claude
subscription.** Two reasons:
- Subscription usage caps are shared across everything using that login. A client's bot
  hitting a burst of tool calls can throttle *your own* usage, and vice versa.
- Anthropic's consumer subscription terms are scoped around individual interactive use
  (Claude.ai / Claude Code), not unattended commercial automation for a third party.
  Running a client's product on your personal Pro/Max/Team plan is a gray area worth
  avoiding rather than relying on.

**Correct setup per new client:**
1. Create a dedicated OS user for the client (mirrors the existing `hermes` /
   `rishab` split) — own `~/.hermes` home, own systemd unit
   (`hermes-gateway-<client>.service`, copy the pattern from
   `/etc/systemd/system/hermes-gateway-rishab.service`).
2. The client provides (or you provision, billed to them) their **own** Claude
   subscription or their **own** OpenRouter/Anthropic API key — never yours.
3. Apply the §2 efficiency config (`auxiliary.background_review` + `fallback_model`)
   as part of onboarding, not as a reactive fix after a cost spike.
4. If using subscription auth for their instance, run `claude /login` as *their* OS user
   with *their* account, and verify with the §3 stripped-env test.
5. Confirm the two OpenRouter/Anthropic API keys (primary account, fallback) are
   genuinely separate from every other client's and from your own personal one —
   check `.env` key fingerprints (last 6-8 chars) don't collide across instances.
6. The client's Claude account must have extra usage enabled and funded (§3). If it
   doesn't, every call is rejected and traffic silently fails over to the OpenRouter
   fallback at metered rates — watch for `Fallback to openrouter` in `agent.log`.

## 5. Stray gateways (duplicate replies)

Symptom: every Discord message gets two replies from the same bot, one from an old model.
Cause found 2026-10-02: a leftover **root** gateway (`/root/.hermes`, Gemini 2.5 Flash via
OpenRouter) running from `/root/.config/systemd/user/hermes-gateway.service` with
`Restart=always` — killing the PID just respawned it. Check for these any time replies
double up or an unexpected model shows in logs:

```bash
ps -eo pid,user,lstart,cmd | grep 'gateway run' | grep -v grep   # expect one per instance
XDG_RUNTIME_DIR=/run/user/0 systemctl --user list-units 'hermes*'  # root's user units
```
Stop it properly with `systemctl --user stop` and `disable` for that unit, not `kill`.
