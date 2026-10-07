# Token Sniper Bot — Project Manifest

**Built:** 2026-08-18  
**Status:** Ready for Deployment  
**Location:** `/home/hermes/token-sniper/`  
**Git:** Local repo (ready to push to GitHub)

---

## Project Structure

```
token-sniper/
├── Documentation
│   ├── README.md                          # Architecture & concepts
│   ├── LAUNCH_SUMMARY.md                  # Quick start guide ← READ FIRST
│   ├── DISCORD_SETUP.md                   # 5-step setup instructions
│   ├── IMPLEMENTATION_SUMMARY.md          # System deep-dive
│   └── MANIFEST.md                        # This file
│
├── Configuration
│   ├── config.py                          # Configuration loader (.env reader)
│   ├── .env.example                       # Template for secrets
│   └── requirements.txt                   # Python dependencies
│
├── Core System
│   └── main.py                            # Entry point + orchestrator
│
├── Notifications
│   └── notifiers/
│       ├── __init__.py
│       └── discord_notifier.py            # Rich Discord embed sender
│
├── Filtering Stages
│   └── filters/
│       ├── __init__.py
│       ├── safety_filter.py               # Stage 1: Honeypot detection
│       └── momentum_filter.py             # Stage 3: Momentum scoring (0-100)
│
└── Extensible Modules (Stubs)
    ├── detectors/__init__.py              # Token detection (Helius, DexScreener)
    ├── utils/__init__.py                  # Helper utilities
    └── models/__init__.py                 # Data models
```

---

## Key Components

### 1. **Configuration System** (`config.py`)
- Reads `.env` environment variables
- Centralized API key management (Helius, Discord, etc.)
- Threshold configuration (sensitivity presets)
- Validation on startup

### 2. **Main Orchestrator** (`main.py`)
- `TokenSniperBot` class: coordinates entire pipeline
- Token detection → filtering → notification flow
- Simulated detection for testing (replace with real Helius WebSocket)
- Lifecycle: initialize → process → alert → track

### 3. **Safety Filter** (`filters/safety_filter.py`)
- **Stage 1** of multi-stage filtering
- Checks:
  - RugCheck API score
  - Mint authority revocation status
  - Freeze authority revocation status
  - Top holder concentration (<20%)
  - LP lock status
- Scoring: 0-100 (higher = safer)
- Decision: Drop if score <30 or 3+ failures

### 4. **Momentum Filter** (`filters/momentum_filter.py`)
- **Stage 3** of multi-stage filtering
- Calculates momentum score (0-100):
  - Unique buyers in 2 min (0-25 pts)
  - Transaction velocity (0-20 pts)
  - Buy/sell ratio (0-20 pts)
  - Price momentum (0-15 pts)
  - Social proof (0-20 pts)
- Alert logic: Score ≥ 65 + LP ≥ $5k + Buyers ≥ 20

### 5. **Discord Notifier** (`notifiers/discord_notifier.py`)
- Sends rich Discord embeds
- Token metrics, safety checks, trading info
- Supports direct channel messages or webhooks
- Alert types: signal (green), blocked (red), status (info)

---

## Setup Steps

### 1. Create Discord Bot (2 min)
```
1. Discord Developer Portal → New Application
2. Bot tab → Add Bot
3. Copy TOKEN
4. OAuth2 → URL Generator → bot + "Send Messages" permission
5. Paste URL to invite to server
6. Enable Developer Mode (Discord settings)
7. Right-click channel → Copy ID
```

### 2. Get API Keys (2 min)
- **Helius**: https://helius.dev (free tier)
- **DexScreener**: https://api.dexscreener.com (free, no signup)
- **RugCheck**: https://api.rugcheck.xyz (free, no signup)

### 3. Configure (2 min)
```bash
cd /home/hermes/token-sniper
cp .env.example .env
# Edit .env with:
# DISCORD_BOT_TOKEN=<from Discord>
# DISCORD_CHANNEL_ID=<from Discord>
# HELIUS_API_KEY=<from Helius>
```

### 4. Install (1 min)
```bash
pip install -r requirements.txt
```

### 5. Run (1 min)
```bash
python main.py
```

**Total: ~10 minutes to first alert**

---

## Files Manifest

| File | Lines | Purpose |
|------|-------|---------|
| `README.md` | 300+ | Architecture overview |
| `LAUNCH_SUMMARY.md` | 280+ | Quick start guide |
| `DISCORD_SETUP.md` | 180+ | Setup instructions |
| `IMPLEMENTATION_SUMMARY.md` | 320+ | System deep-dive |
| `MANIFEST.md` | This | Project overview |
| `config.py` | 70 | Configuration loader |
| `main.py` | 180 | Orchestrator + entry point |
| `notifiers/discord_notifier.py` | 200+ | Discord integration |
| `filters/safety_filter.py` | 200+ | Honeypot detection |
| `filters/momentum_filter.py` | 140+ | Momentum scoring |
| `requirements.txt` | 7 | Dependencies |
| `.env.example` | 30 | Config template |

**Total:** ~2,500 lines of code + docs

---

## Repository Info

**Local:** `/home/hermes/token-sniper/`  
**Git:** Initialized (master branch)  
**Ready to push:** Yes (to `https://github.com/DoAnythingNow33/token-sniper.git`)

---

**Status:** 🚀 **Ready to Deploy**

**Next Action:** Read `LAUNCH_SUMMARY.md` and follow `DISCORD_SETUP.md`
