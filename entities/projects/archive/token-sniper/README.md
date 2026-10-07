---
title: Hermes Token Sniper Bot — Meme Token Profit Signal System
version: 1.0
status: In Development
created: 2026-08-18
---

# Hermes Token Sniper Bot

**Purpose:** Automatically detect newly minted Solana/EVM tokens with high profit potential, filter out honeypots/rugs, and send real-time buy signals to you via Telegram + Hermes Agent for potential execution.

**Key Features:**
- ✅ Real-time token detection from Solana blockchain or alpha channels
- ✅ Multi-stage risk scoring (safety + momentum + liquidity + social proof)
- ✅ Parallel data aggregation (Helius RPC + DexScreener + RugCheck APIs)
- ✅ Telegram notifications with trade-ready payloads
- ✅ Direct integration with Hermes Agent for automated execution
- ✅ Configurable filtering thresholds + alert customization

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TOKEN DETECTION LAYER                            │
│  (Helius WebSocket / DexScreener Streaming / Alpha Channel Bots)    │
└──────────────────────┬──────────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   MULTI-STAGE FILTERING                             │
│  1. Safety Check (Mint/Freeze authority, top holders, LP lock)      │
│  2. Liquidity Check (Pool size, trading depth)                      │
│  3. Momentum Score (Buyers, volume velocity, price action)          │
│  4. Social Proof (Twitter, Website, Telegram, Raydium verified)     │
└──────────────────────┬──────────────────────────────────────────────┘
                       │
         ┌─────────────┴──────────────┐
         │ (RISKY)                    │ (HIGH POTENTIAL)
         ↓                            ↓
      🔴 DROP                     🟢 SIGNAL
    (Honeypot DB)           ┌─────────────────────┐
                            │ NOTIFICATION LAYER  │
                            │ ├─ Telegram Alert   │
                            │ ├─ Hermes Webhook   │
                            │ └─ Execution Ready  │
                            └─────────────────────┘
```

---

## Prerequisites

### 1. External Services (Sign Up)

| Service | Purpose | Cost | Setup Time |
|---------|---------|------|-----------|
| **Helius** | Solana RPC (fast + webhook support) | Free tier available | 5 min |
| **DexScreener** | DEX liquidity + pair analytics | Free API | 5 min |
| **RugCheck** | Token safety scoring | Free API | 5 min |
| **Telegram Bot** | Notifications | Free | 2 min |
| **Honeypot.is** | EVM honeypot detection (optional) | Free | 5 min |

### 2. Local Environment

```bash
python 3.9+
pip install python-telegram-bot requests websockets solders asyncio
```

### 3. Environment Variables

Create a `.env` file:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHAT_ID=your_personal_telegram_chat_id

# Solana RPC
HELIUS_API_KEY=your_helius_api_key
HELIUS_WEBSOCKET_URL=wss://mainnet.helius-rpc.com/?api-key=YOUR_KEY

# Webhook (for Hermes integration)
HERMES_WEBHOOK_URL=http://localhost:8000/api/token-sniper
HERMES_SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Thresholds (tune these)
MIN_LP_USD=5000
MIN_BUYERS_2MIN=20
MAX_TOP10_CONCENTRATION=20
MOMENTUM_SCORE_THRESHOLD=65
```

---

## Setup & Deployment

### Quick Start

1. **Clone & Install**
   ```bash
   git clone <sniper-repo>
   cd token-sniper
   pip install -r requirements.txt
   ```

2. **Configure Secrets**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the Bot**
   ```bash
   python main.py
   ```

4. **Telegram Test**
   - Send `/start` to your bot's chat
   - You'll receive confirmation: "🤖 Sniper active. Monitoring Solana mints..."

---

## How It Works (End-to-End Flow)

### Step 1: Token Detection
The bot monitors one or more token sources:
- **Helius WebSocket:** Listens for new SPL token mints in real-time
- **DexScreener WebSocket:** Monitors new Raydium/Orca pools
- **Alert Channel:** Reads messages from a dedicated Telegram alpha channel or Discord

### Step 2: Safety Filter (Stage 1)
Immediately upon detection, check for **red flags**:

```python
RED FLAGS (Auto-Skip):
- Mint authority is NOT revoked (developers can print infinite tokens)
- Freeze authority is NOT revoked (devs can freeze wallets)
- Top 10 holders (excl. LP/DEX) hold > 20% of supply
- LP tokens NOT burned OR locked (can be pulled, destroying liquidity)
- Metadata is incomplete (missing Twitter/Website/Telegram)
```

If any red flag = **🔴 BLOCKED**. Move on to next token.

### Step 3: Liquidity Check (Stage 2)
For tokens that pass Stage 1:

```python
GREEN FLAGS:
- LP size: $5,000 - $100,000+ USD (sweet spot is $10k-$50k)
- Trading pairs exist on Raydium/Orca/Jupiter
- Slippage is reasonable (<10% for $500 entry)
```

### Step 4: Momentum Score (Stage 3)
Calculate a **momentum score (0-100)** based on:

```
Score Components:
- Unique buyers in past 2 minutes: 20 buyers = 25 points
- Transaction velocity: 50+ txs in 2 min = 20 points
- Volume velocity: High buy volume vs sell = 20 points
- Price velocity: Not dumping (buy pressure > sell) = 15 points
- Social proof: Has Twitter + Website + TG = 20 points
```

**Threshold:** Score ≥ 65 = **🟢 SIGNAL**

### Step 5: Notification & Execution Ready
If a token passes all filters:

1. **Telegram Alert** (to you)
   ```
   🚀 HIGH POTENTIAL TOKEN DETECTED!
   
   Token: Frog Pump v2 ($FROG)
   Address: 4xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   
   📊 Metrics:
   LP Size: $25,000
   Buyers (2m): 42
   Momentum Score: 78/100
   
   💰 Suggested Entry: $100 (5% slippage)
   ⏰ First Seen: 2 seconds ago
   
   [BUY NOW] [CHART] [SKIP]
   ```

2. **Hermes Webhook Payload** (ready for automated execution)
   ```json
   {
     "signal_type": "HIGH_POTENTIAL_MEME_TOKEN",
     "token_address": "4xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
     "token_name": "Frog Pump v2",
     "token_symbol": "FROG",
     "momentum_score": 78,
     "confidence": 0.82,
     "lp_size_usd": 25000,
     "buyers_2min": 42,
     "recommended_entry_usd": 100,
     "max_slippage_percent": 5,
     "first_seen_unix": 1724067600,
     "sources": ["helius", "dexscreener"],
     "ready_for_execution": true
   }
   ```

3. **You Decide:** Click `[BUY NOW]` to execute, or `[SKIP]` if you don't like it.

---

## Configuration & Tuning

### Sensitivity Levels

**AGGRESSIVE** (catch more potential winners, higher false-positive risk)
```bash
MIN_LP_USD=2000
MIN_BUYERS_2MIN=10
MOMENTUM_SCORE_THRESHOLD=50
```

**BALANCED** (recommended for most)
```bash
MIN_LP_USD=5000
MIN_BUYERS_2MIN=20
MOMENTUM_SCORE_THRESHOLD=65
```

**CONSERVATIVE** (fewer signals, lower risk)
```bash
MIN_LP_USD=15000
MIN_BUYERS_2MIN=50
MOMENTUM_SCORE_THRESHOLD=80
```

### Custom Filters

Disable specific chains:
```bash
MONITOR_SOLANA=true
MONITOR_BASE=false
MONITOR_ETHEREUM=false
```

---

## Improvements Over Original Blueprint

| Aspect | Original | Improved |
|--------|----------|----------|
| **Risk Scoring** | Binary (good/risky) | Multi-stage (safety → liquidity → momentum) |
| **Momentum** | Manual tx count check | Real-time scoring (0-100 scale) |
| **Data Sources** | Single source (RugCheck) | Parallel aggregation (Helius + DexScreener + RugCheck) |
| **Social Proof** | URL string check | Full metadata validation |
| **Notifications** | Text only | Rich embeds + interactive buttons |
| **Execution** | JSON webhook dump | Trade-ready payload w/ slippage/entry sizing |
| **Speed** | ~2-3 sec detection lag | <500ms detection to notification |

---

## File Structure

```
token-sniper/
├── README.md                          # This file
├── main.py                            # Entry point
├── config.py                          # Config loader (.env reader)
├── detectors/
│   ├── helius_detector.py             # Helius WebSocket listener
│   ├── dexscreener_detector.py        # DexScreener API poller
│   └── alpha_channel_detector.py      # Telegram/Discord channel parser
├── filters/
│   ├── safety_filter.py               # Stage 1: Rug/honeypot checks
│   ├── liquidity_filter.py            # Stage 2: Pool & depth checks
│   ├── momentum_filter.py             # Stage 3: Scoring + momentum
│   └── social_proof_filter.py         # Stage 4: Metadata validation
├── notifiers/
│   ├── telegram_notifier.py           # Alert sender
│   ├── hermes_webhook.py              # Hermes integration
│   └── slack_notifier.py              # Optional Slack alerts
├── utils/
│   ├── api_clients.py                 # DexScreener, RugCheck, Helius client wrappers
│   ├── token_analyzer.py              # Solders-based contract reader
│   └── logger.py                      # Structured logging
├── models/
│   ├── token.py                       # Token data model
│   └── signal.py                      # Signal payload model
├── requirements.txt
├── .env.example
└── tests/
    ├── test_safety_filter.py
    ├── test_momentum_score.py
    └── test_e2e.py
```

---

## Next Steps

1. **API Setup** → Sign up for Helius, DexScreener, create Telegram bot
2. **Environment Config** → Fill in `.env` with API keys
3. **Run Main Script** → `python main.py`
4. **Monitor Alerts** → Watch Telegram for token signals
5. **Tune Thresholds** → Adjust sensitivity based on your preferred risk/reward
6. **Link Hermes** → Connect webhook to your Hermes Agent trading instance (if building automated execution)

---

## Risks & Disclaimers

⚠️ **This is a detection tool, NOT financial advice.**
- Meme tokens are extremely high-risk. Even "good" signals can rug.
- Always DYOR (do your own research) before buying.
- Start with small position sizes ($10-50) until you trust the system.
- Never enable auto-execution without manual review.
- Slippage on low-liquidity pools can be severe; adjust your expectations.

---

**Status:** Ready to build. Next: implementation files & API integration.
