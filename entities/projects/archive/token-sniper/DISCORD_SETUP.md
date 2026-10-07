# Token Sniper Bot - Discord Setup Guide

## Prerequisites

You'll need:
1. **Discord Server** (yours already - DoAnythingNow.)
2. **Discord Bot Token** (from Discord Developer Portal)
3. **Helius API Key** (Solana RPC)
4. **API Keys**: DexScreener (free), RugCheck (free)

---

## Step 1: Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** → name it "Token Sniper"
3. Go to **"Bot"** → click **"Add Bot"**
4. Under **"TOKEN"** → copy the token
   ```
   DISCORD_BOT_TOKEN=YOUR_TOKEN_HERE
   ```
5. Go to **"OAuth2" → "URL Generator"**:
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Embed Links`, `Read Message History`
   - Copy generated URL
6. Paste URL in browser to invite bot to your Discord server

---

## Step 2: Get Channel ID

1. Enable **Developer Mode** in Discord (User Settings → Advanced → Developer Mode)
2. Right-click the token sniper channel → **Copy Channel ID**
   ```
   DISCORD_CHANNEL_ID=YOUR_CHANNEL_ID
   ```

---

## Step 3: Setup API Keys

### Helius (Solana RPC)
1. Go to [helius.dev](https://helius.dev)
2. Sign up → get free API key
   ```
   HELIUS_API_KEY=YOUR_KEY
   HELIUS_WEBSOCKET_URL=wss://mainnet.helius-rpc.com/?api-key=YOUR_KEY
   ```

### DexScreener (Free)
- No signup needed, free API at `https://api.dexscreener.com/latest/dex`

### RugCheck (Free)
- Free API at `https://api.rugcheck.xyz/v1/tokens`

---

## Step 4: Create `.env` File

```bash
# Discord
DISCORD_BOT_TOKEN=MzA4MzMxMzMwNzE0NzU4NjU2.YOUR_BOT_TOKEN_HERE
DISCORD_CHANNEL_ID=1234567890
DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/YOUR_WEBHOOK

# Solana
HELIUS_API_KEY=YOUR_HELIUS_API_KEY
HELIUS_WEBSOCKET_URL=wss://mainnet.helius-rpc.com/?api-key=YOUR_HELIUS_API_KEY

# Thresholds
MIN_LP_USD=5000
MIN_BUYERS_2MIN=20
MOMENTUM_SCORE_THRESHOLD=65
MAX_TOP10_CONCENTRATION=20

# Hermes Integration (optional)
HERMES_WEBHOOK_URL=http://localhost:8000/api/token-sniper

# Monitoring
MONITOR_SOLANA=true
MONITOR_BASE=false
ALERT_ON_HIGH_MOMENTUM=true
```

---

## Step 5: Install & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

You should see:
```
✅ Discord bot ready as Token Sniper#1234
✅ Listening on Helius for new Solana mints...
ℹ️ Monitoring 1,234 existing tokens
```

---

## What You'll See

### 1. High-Potential Token Alert
When a token passes all filters:

```
🚀 Frog Pump v2 ($FROG)
High-potential meme token detected!

📊 Key Metrics
Momentum Score: 78/100
LP Size: $25,000
Buyers (2m): 42
Time Seen: 2s ago

✅ Safety Checks
Mint Authority Revoked: ✅
Freeze Authority Revoked: ✅
LP Locked: ✅
Social Verified: ✅

💰 Suggested Entry
$100 (Max 5% slippage)

📍 Token Address
4xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

🔗 Links
[Twitter] | [Website] | [Chart]

Confidence: 82% | Sources: helius, dexscreener
```

### 2. Blocked Token (with reason)
When a token is unsafe:

```
🔴 Token Blocked
Freeze authority is open (devs can freeze wallets)

Token Address: 5xYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
Mint Authority Revoked: No
RugCheck Score: 750 (High Risk)
```

### 3. Status Updates
```
ℹ️ INFO
Sniper online. Monitoring 2,345 tokens. Ready to alert on high-momentum mints.
```

---

## Configuration Presets

### 🔥 AGGRESSIVE (Catch more, higher risk)
```bash
MIN_LP_USD=2000
MIN_BUYERS_2MIN=10
MOMENTUM_SCORE_THRESHOLD=50
```

### ⚖️ BALANCED (Recommended)
```bash
MIN_LP_USD=5000
MIN_BUYERS_2MIN=20
MOMENTUM_SCORE_THRESHOLD=65
```

### 🛡️ CONSERVATIVE (Fewer but safer)
```bash
MIN_LP_USD=15000
MIN_BUYERS_2MIN=50
MOMENTUM_SCORE_THRESHOLD=80
```

---

## Troubleshooting

**Bot doesn't send messages:**
- Check DISCORD_CHANNEL_ID is correct
- Verify bot has "Send Messages" permission in channel
- Check bot is in the server

**No tokens being detected:**
- Verify HELIUS_API_KEY is valid
- Check Helius quota (free tier: 1M RPC calls/month)
- Solana network might be slow

**All tokens getting blocked:**
- Lower MOMENTUM_SCORE_THRESHOLD
- Check RugCheck API is responding
- Verify Solana network is healthy

---

## Next Steps

1. **Let it run for 24 hours** and see what signals you get
2. **Tune thresholds** based on signal quality
3. **Add Hermes webhook** if you want semi-automated execution
4. **Create trading backtest** to validate signal profitability

---

**Status:** Ready to deploy 🚀
