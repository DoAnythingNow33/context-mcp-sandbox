---
entity: Token Sniper
type: snapshot
last_updated: 2026-10-05
current_state: "**ARCHIVED 2026-10-05 — Dan shut the bot down and archived the project.** Code, docs, outcomes.jsonl and full git history (token-sniper.bundle) are in entities/projects/archive/token-sniper/; no secrets included. Everything below is the state as of 2026-08-31. Personal side project — a live Discord bot watching Solana pump.fun launches via a Helius websocket, evaluating each survivor at +30min and posting passes to #buy-token. **v2 filter stack shipped + deployed live 2026-08-31** (commit b5636e5 on the box repo; v1 backed up to token-sniper-backup-v1-pre-v2-20260831-0940.tgz). New cost-ordered pipeline: L1 sellability (pump.fun frontend-api-v3 + Jupiter lite-api sell-sim + migrated-only gate + hidden/nsfw reject) → safety (mint/freeze authority) → L3 spam (RugCheck now a hard-fail, in-process ticker-farm tracker) → one Helius DAS holder read → L2 wash-detection (sell-side flow 15–60%, volume/LP ≤8, ≥30 distinct holders, hard-dump −20% fail; raw tx-count and buy-ratio dropped as positive drivers). L4 social gate still deferred. Layer 5 feedback loop live: every decision (alert + reject) → data/outcomes.jsonl, alerts price-polled at +1/6/24h to a persistent watchlist. All four v1 false positives (beanly/USMS/MRHATE/Rabbit) verified rejected offline; all v2 APIs confirmed working at \\$0. Expect near-zero alerts for a while — migrated-only + wash gates are strict by design. This is the test of whether any edge exists."
current_focus:
  - "Let v2 run 3–5 days and read data/outcomes.jsonl — which layer/threshold actually predicts the +1/6/24h outcome. Stop guessing at thresholds."
  - "Then build Layer 4 (free social proxy: pump.fun reply_count + linked-Twitter-resolves hard gate)."
open_questions:
  - "Does ANY combination of free filters produce a positive-EV signal on +30min pump.fun tokens, or is the honest answer 'this class of token is not worth sniping'? Layer 5 data over the next week is the test."
  - "Is the migrated-only gate too strict — does it starve the signal entirely? REJECT_PRE_MIGRATION=true for now; revisit against outcome data."
  - "Free X/Twitter search is effectively dead. Is the free social proxy good enough as a hard gate, or does real signal need paid X search (deferred until winners)?"
tensions:
  - "Dan wants 100%+ gain candidates; the pipeline can only ever filter for 'sellable + not obviously wash + real holder count'. Both $5 buys going to zero is the concrete cost of that gap."
  - "'Strictly free until we get winners' vs. the best social signal (X contract-address search) being paid-only. v2 uses free proxies; real X search stays a documented Phase-2 upgrade."
next_actions:
  - "Rotate DISCORD_BOT_TOKEN and HELIUS_API_KEY — still outstanding"
  - "Check #buy-token + data/outcomes.jsonl after ~3 days; tune L2 thresholds against the poll results"
  - "Build Layer 4 free social proxy once there's outcome data to justify thresholds"
---

# Token Sniper

**Relationship:** Personal side project — Dan's own experiment, unrelated to DoAnythingNow client work
**Role:** Builder/operator

## What it is

A Discord bot that watches new token launches on pump.fun (Solana) live and alerts on ones that pass safety + momentum checks. Not a DoAnythingNow deliverable — built as a personal trading-signal tool, documented here per the vault's own rule that anything Dan is responsible for gets tracked, and because it lives on the same server infrastructure (`5.75.188.204`, the Hetzner box that also runs Hermes) and is worth having discoverable context on.

## Architecture

- **Detection**: `detectors/pumpfun_detector.py` — subscribes to Solana mainnet via a Helius websocket (`logsSubscribe`, confirmed commitment). The new mint is decoded directly from pump.fun's Anchor `CreateEvent` in the `Program data:` log line carried in the notification itself (`utils/pumpfun_event.py`, discriminator `1b72a94ddeeb6376`, borsh: name/symbol/uri strings then mint/bonding_curve/user pubkeys). **No `getTransaction` / `getMultipleAccounts` follow-up** — detection costs zero RPC credits. (Previously it fetched + batch-decoded the whole triggering tx on every launch, ~2 Helius calls each at ~50 launches/min — the real credit burn.)
- **Cheap pre-filter (free)**: waits ~5 min (`PREFILTER_WAIT_SEC=300`), checks DexScreener for min buys + liquidity. Drops the dead-on-arrival majority so they aren't tracked through the aging window.
- **Aging wait**: survivors are held until `EVAL_DELAY_SEC` after mint (default **1800 = 30 min**; 3600 for 1 h) before anything is judged. Rationale (Dan, 2026-08-30): a freshly-minted token always trips holder-concentration risks and has thin trading data — evaluating at +30 min gives a far more honest read, and early snipers have usually exited by then.
- **Safety filter** (`filters/safety_filter.py`, runs once at +30 min — one `getAccountInfo`, the bot's only on-chain read): RugCheck API report, on-chain mint/freeze authority. **Open mint or freeze authority is a hard fail** (not a score deduction) — as is an unreadable mint. RugCheck `danger` risks hard-fail unless named in `SAFETY_IGNORED_RISKS`. LP-lock inferred from RugCheck's risk list (soft signal). Top-holder concentration is **not** checked directly — Helius's `getTokenLargestAccounts` rejects Token-2022 mints (all of pump.fun).
- **Momentum scoring** (`filters/momentum_filter.py`, pre-existing): buyer count, tx velocity, buy/sell ratio, price momentum, social proof — DexScreener-backed (its finest bucket is 5 minutes, used as an honest proxy for "since launch," not a literal 2-minute window).
- **Notification split** (wired 2026-08-30): passing signals → `#buy-token` (`DISCORD_CHANNEL_ID=1543609479633961051`); blocked tokens + bot status → `#token-sniper` (`DISCORD_BLOCKED_CHANNEL_ID=1543593379625967626`, mute this one).
- **Persistence**: `deploy/token-sniper.service`, a user-level systemd unit under the `hermes` Linux user (no root needed — lingering enabled so it survives logout/reboot).

## Known, deliberate limitations

- Top-holder concentration always reads "unknown" for pump.fun tokens (see above) — degrades safely rather than lying about a check it can't run.
- LP-lock status is inferred from RugCheck's risk feed, not independently verified on-chain — real verification would need per-AMM pool parsing (Raydium/Meteora/pump.fun all differ).
- The Discord embed deliberately does not show a fabricated "recommended entry price" or "confidence %" — the original scaffold had these hardcoded as placeholder numbers; presenting invented figures as financial guidance was judged actively harmful, so they were dropped in favor of only real, measured values.

## Repo

`/home/hermes/token-sniper` on the Hetzner box (separate git repo from Context 2.0, no remote — local history only). `.env` holds secrets and is gitignored. Pre-audit state backed up to `/home/hermes/token-sniper-backup-*.tgz` and `.env.bak`.

## Audit (2026-08-30)

Full code audit + rework. Fixed: (1) per-launch Helius cost — detection was resolving every launch on-chain before any filtering; now parses the mint from the websocket event log, zero RPC. (2) Safety hole — a token with open mint authority could pass if RugCheck/LP data were merely missing; open authority is now a hard fail. (3) `.env` was missing `PREFILTER_*` / `MOMENTUM_WAIT_SEC` / `DISCORD_BLOCKED_CHANNEL_ID` (defaults were silently used); dead config removed (Telegram, Slack, Hermes webhook, chain-monitor flags). (4) Momentum filter: fake volume-weighted buy/sell ratio replaced with honest tx-count ratio; `MIN_LP_USD` now respected instead of a hardcoded 5000. Mechanism for the timing/concentration tradeoff added as config (`SAFETY_IGNORED_RISKS`, `RUGCHECK_MAX_SCORE`).

**Follow-up same day:** on Dan's call, moved evaluation from +45s to +30min (`EVAL_DELAY_SEC=1800`) — safety + momentum now run once on an aged token instead of a freshly-minted one — and wired the real `#buy-token` / `#token-sniper` channel IDs.

---

## v2 Plan (2026-08-31)

### Why v1 fails — from the first 20h of real data

178 alerts / 20h. Representative passes:

| Token | buy txns (5m) | total txns | buy ratio | price | socials |
|---|---|---|---|---|---|
| beanly | 1,890 | 1,922 | 98% | +15% | none |
| USMS | 495 | 501 | 99% | +1.4% | none |
| MRHATE | 2,612 | 3,497 | 75% | +42% | none |
| Rabbit | 1,634 | 2,720 | 60% | **−34%** | Twitter+site |

Three root causes:

1. **Momentum filter rewards wash trading.** It scores transaction *count* and buy *ratio* — both trivially inflated by a volume bot. A 98% buy ratio (nobody taking profit) scores 20/20 when it should be disqualifying. Copycat ticker farms (USMS/USWS variants) relaunch repeatedly with nothing to dedupe them.
2. **Nothing checks whether you can sell.** Both of Dan's $5 buys pumped on paper then went to zero — no liquidity / abandoned. Safety filter has no concept of sellability.
3. **Socially dead tokens pass freely.** Almost every signal has `social: 0/20 (None)`. A memecoin with real momentum has someone posting the contract address.

### What a bonding curve is (context for the "hidden, low-liquidity, couldn't sell" tokens)

A pump.fun token doesn't launch with a normal liquidity pool. It launches on a **bonding curve** — a smart contract acting as an automated market maker with a fixed price formula. Buys push price up the curve, sells push it back down; all the "liquidity" is the SOL sitting in that curve contract. When the curve fills (~$69k mcap historically; pump.fun tunes this), the token **"migrates" / "graduates"** — pump.fun moves the liquidity into a real AMM (pump.fun's own PumpSwap, formerly Raydium) and burns the LP tokens. After that it trades like any AMM token.

Implications:
- **Pre-migration**: you can always sell back to the curve at the formula price, but if the token is low on the curve the SOL you get back is tiny, and Jupiter/DexScreener routing is patchy.
- **Post-migration with thin liquidity**: the deployer/snipers can still dump or the pool can be near-empty. This is the "going up but couldn't sell" trap Dan hit.
- pump.fun's own `frontend-api.pump.fun/coins/{mint}` (free, unofficial) exposes `complete` (migrated?), `hidden`, `nsfw`, `reply_count`, market cap, creator, and linked socials — directly useful, including for the "hidden on the platform" flag.

### Locked decisions (Dan, 2026-08-31)

- **Position size: $5.** So liquidity *depth* is a near-non-issue — $5 exits almost anything. The Layer 1 sell-sim therefore serves as a **honeypot / can-I-sell-at-all check** (transfer tax, sell-disabled, no route), not a depth check. The high-value levers at this size are **Layer 2 (wash detection)** and **Layer 4 (social gate)** — filtering fake/abandoned tokens, not thin ones.
- **X social = hard gate** (no social footprint → no alert).
- **Strictly free APIs until the bot produces winners.** No Birdeye paid, no X API paid. Free-tier only.
- **Save this plan; Dan implements in a new session.**

### Free API stack to build on (evaluate each at $0 first)

- **Jupiter Quote API** — free. Sell-route / honeypot simulation.
- **DexScreener** — free, already used. Liquidity, volume, txns, `dexId` (migration), socials.
- **RugCheck** — free, already used. Risk report + score.
- **pump.fun `frontend-api.pump.fun/coins/{mint}`** — free/unofficial. Migration status, `hidden`/`nsfw` flags, reply count, creator, socials.
- **Helius** — already have credits. DAS `getTokenAccounts` (holder enumeration, works for Token-2022), parsed tx history (dev-wallet dump detection).
- **Candidates Dan has seen / worth checking free tiers:** Solana Tracker (`data.solanatracker.io` — free tier ~1 req/s, risk + holders + pools + ATH), Birdeye free tier (holder count, security), Moralis Solana API free tier. Confirm what each returns at $0 before wiring.
- **X/Twitter**: no usable free search API. `snscrape`/nitter are effectively dead. So the free social gate uses **proxies**: pump.fun `reply_count` threshold + the token's linked Twitter resolves (unauthenticated `publish.twitter.com/oembed`) and isn't zero-follower. Real X contract-address search is a **Phase 2 upgrade, deferred until winners** (then ~$0.15–0.40/1k posts via a third-party scraper, or $200/mo official).

### The layers (priority order for $5 / free)

**Layer 1 — Sellability / honeypot (free, deterministic).**
- Jupiter: can a sell of the full position route at all? Reject if no route or if round-trip loss > ~15% (still meaningful even at $5 — catches transfer tax / sell traps).
- Reject pump.fun `hidden` / `nsfw` tokens outright.
- Keep a real liquidity floor but modest (~$10k) since size isn't the constraint; main use is sanity, not depth.
- Migration policy: **reject pre-migration (on-curve) tokens by default** (`dexId`/`complete` check), revisit later. Simpler and cuts a big chunk of junk.

**Layer 2 — Wash-trade / fake-momentum (rewrite `momentum_filter.py`).**
- **Require sell-side flow**: sells must be ~15–45% of transactions. A >95% buy ratio flips from bullish to *rejected*.
- **Volume / liquidity ratio cap**: huge 5-min volume against a small pool = wash. Reject above a ratio.
- **Unique maker wallets, not tx count**: pull distinct buyers (Helius tx parse or a free-tier API). Gate on ~25–40 real wallets. If thousands of txns came from a dozen wallets, reject.
- **Hard dump = hard fail**: < ~−20% at eval → reject (Rabbit alerted at −34%).
- Drop raw tx-count and buy-ratio as *positive* score drivers.

**Layer 3 — Spam / rug lists (free, high signal).**
- Phantom / Blowfish blocklist lookup → hard reject if flagged. (Confirm free access.)
- RugCheck score over cap becomes a **hard fail** (currently soft −50; half the v1 passes sit at score 50).
- Repeat-symbol heuristic: track tickers seen in the last N hours; a symbol relaunching many times/day is a farm — skip or require a far higher bar.
- Dev-wallet check: creator wallet (known from CreateEvent) already dumped? Helius parsed history.

**Layer 4 — Social hard gate (free proxy version).**
- pump.fun `reply_count` ≥ threshold (e.g. 20–50 real replies), AND
- token's linked Twitter/X account resolves + isn't brand-new / zero-follower, AND
- (Phase 2, paid, deferred) X search for the contract address: ≥3 distinct credible authors in the last hour, follower-weighted, velocity rising.
- No social footprint → no alert, full stop.

**Layer 5 — Feedback loop (build alongside Layers 1–3).**
- Log every alert with entry price, LP, `dexId`, and every filter value.
- Poll price at +1h / +6h / +24h (DexScreener, cheap) onto a small watchlist.
- After 3–5 days, this data says which layer actually predicts outcome — stop guessing at thresholds.

### Honest note

Even fully built this is a game with a structural edge against a retail sniper. Realistic goal: turn ~178 garbage alerts/day into a handful that are at least sellable, non-wash, and socially real. It cannot manufacture winners. Treat the v2 build as the test of whether any edge exists here at all — if a week of Layer-5 data shows the filtered signals still lose, that's the answer.

### Build order

1. Layers 1 + 2 + 3 + 5 (free, deterministic, no new paid deps) → kills most false positives, adds the feedback loop.
2. Run 3–5 days. Read the outcome data.
3. Build Layer 4 free proxy. Re-assess.
4. Only if there are winners: paid X contract-address search.

### Still-open decisions for the build session

- Exact thresholds (sell-side %, vol/liq ratio, unique-maker count, reply count) — set provisionally, tune against Layer-5 data.
- Which free-tier API wins for unique-maker / holder data (Solana Tracker vs Birdeye free vs Helius parse).
- Whether to keep alerting on the v1 logic during the build or pause the bot.

---

## v2 build — shipped 2026-08-31 (commit b5636e5)

Built and deployed live in one session. v1 backed up to `token-sniper-backup-v1-pre-v2-20260831-0940.tgz`.

**New modules:** `detectors/pumpfun_api.py` (frontend-api-v3.pump.fun — migration/hidden/nsfw/reply_count/creator/socials), `detectors/jupiter_client.py` (lite-api.jup.ag sell-sim honeypot check), `detectors/helius_client.py` (DAS `getTokenAccounts` holder enumeration — works for Token-2022), `filters/sellability_filter.py` (L1), `filters/spam_filter.py` (L3 + in-process `SymbolFarmTracker`), `utils/outcome_logger.py` (L5, persistent watchlist). Rewrote `filters/momentum_filter.py` (L2), extended `detectors/dexscreener_client.py` (buys/sells split, dexId/migration, price, SOL price helper).

**Endpoint corrections found during the build:** `quote-api.jup.ag/v6` is dead → `lite-api.jup.ag/swap/v1/quote`. `frontend-api.pump.fun` returns 530 from the box → `frontend-api-v3.pump.fun`. Both free, no key. All in `.env` + `config.py` defaults.

**Decisions locked:** migrated-only gate ON (`REJECT_PRE_MIGRATION=true`). Creator-dump check demoted to a logged field, not a gate — a pump.fun creator holds 0 tokens by default, so "holds zero" is the normal case, not a rug signal. Phantom/Blowfish blocklist left unwired (no confirmed free endpoint) — documented Phase-2 add.

**Config now in `.env`:** `L1_*`, `L2_*`, `RUGCHECK_MAX_NORMALISED`, `SYMBOL_FARM_*`, `OUTCOME_*`; `MOMENTUM_SCORE_THRESHOLD` 65→55, `MIN_LP_USD` 5000→10000.

**Verified:** all 4 v1 false positives rejected by L2 offline (`test_filters.py`); every external API returns real data at $0 (`smoke_v2.py`); service restarted clean, watch loop running.

### Follow-up same day — commit c690cac: dust/Sybil-airdrop gate

First v2 alert (旺财 / WangCai, `Ax3U1fBe…pump`) passed every layer — RugCheck 1/100, 2913 holders, 26% sell-side, vol/LP 1.9, Twitter+site — but **Phantom flags it as spam and won't let Dan buy.** Cause: manufactured holder base — ~2900 wallets each holding ~0.2% of supply. RugCheck doesn't catch this; Phantom's own classifier does.

Fix (L3 / `spam_filter.py`): exclude the AMM pool (pump.fun `pool_address`), then measure real-wallet distribution from the Helius DAS enumeration already being done — largest real wallet as % of supply (`non_pool_top_pct`) + top/10th `flatness_ratio`. Reject if ≥300 holders and largest real wallet <1.2% of supply, or flatness <2.5. Verified: 旺财 rejected (0.58% top wallet), an organic 4800-holder token still passes (6.2% top wallet). Knobs: `AIRDROP_MIN_*` in `.env`.

Lesson for L4/tuning: **holder count is gameable exactly like tx-count was** — a dust airdrop buys 2900 "holders" cheaply. The distribution shape, not the count, is the real signal.

**Next:** 3–5 days of `data/outcomes.jsonl`, then tune thresholds and build L4.

### Outcome data — 2026-09-02 (the experiment's answer)

Funnel over ~2 days: **171 rejected** (101 sellability, 59 spam, 8 safety, 3 momentum), **3 passed**. All 3 alerts went to near-zero:

| Token | entry LP | profile at eval | +24h |
|---|---|---|---|
| 旺财 | $39k | 2900 dust-airdrop holders | **0.01x** (−99%) |
| ODD7 | $22k | thin LP, migrated, socials | **0.036x** (−96%) |
| Mani | $53k | balanced flow (51% sells), 2200 real holders, whale top 12.5% — looked genuinely clean | **0.005x** (−99.5%) |

Three different failure profiles — fake holders / thin LP / textbook-healthy — all −96%+. Phantom independently flags them as spam. The filters work (they reject ~98% of garbage); the residual is also garbage because **the whole population at +30min migrated pump.fun is post-pump dumps**. This is the clean negative result the plan asked for: no free-data edge exists on this class. Chasing the Phantom flag with more free filters is chasing a signal the free data doesn't contain.

**Decision pending (Dan):** stop sniping this class / keep bot as data-only collector / pivot strategy (earlier timing + curve risk, or paid X-traction signal). No more money in until a strategy change. Bot left running alert-only; Dan is not acting on alerts.
