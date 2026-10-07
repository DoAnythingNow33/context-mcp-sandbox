---
title: Token Sniper Bot - INTERACTIVE SETUP (Step-by-Step for Dan)
date: 2026-08-18
status: In Progress
---

# 🚀 TOKEN SNIPER BOT — INTERACTIVE SETUP

**Goal:** Get your bot detecting meme tokens in Discord in ~15 minutes.

---

## ✅ STEP 1: Create Discord Bot (5 minutes)

### 1a. Go to Discord Developer Portal
1. Open **[https://discord.com/developers/applications](https://discord.com/developers/applications)** in your browser
2. Click **"New Application"**
3. Name it: `Token Sniper` (or whatever you prefer)
4. Click **"Create"**

### 1b. Create the Bot User
1. In the left sidebar, click **"Bot"**
2. Click **"Add Bot"**
3. Under **"TOKEN"**, click **"Copy"** to copy your bot token
   ```
   SAVE THIS: Your Discord Bot Token (paste into .env later)
   ```

### 1c. Give Bot Permissions
1. Click **"OAuth2"** in left sidebar
2. Click **"URL Generator"**
3. Under **"SCOPES"**, check: `bot`
4. Under **"PERMISSIONS"**, check:
   - ✅ Send Messages
   - ✅ Embed Links  
   - ✅ Read Message History
5. Copy the **"GENERATED URL"** at the bottom
6. Paste it into a new browser tab to invite the bot to your **DoAnythingNow.** server

**✅ Bot should now appear in your Discord server as "Token Sniper"**

---

## ✅ STEP 2: Get Channel ID (2 minutes)

### 2a. Enable Developer Mode in Discord
1. In Discord, click your **Profile Settings** (⚙️ gear icon, bottom left)
2. Go to **"Advanced"**
3. Toggle **"Developer Mode"** ON

### 2b. Get Your Channel ID
1. In your Discord server, create a new channel called **#token-sniper** (or use existing)
2. Right-click the channel name → **"Copy Channel ID"**
   ```
   SAVE THIS: Your Discord Channel ID (paste into .env later)
   Example: 1234567890123456789
   ```

---

## ✅ STEP 3: Get API Keys (5 minutes)

### 3a. Helius API Key (Solana RPC)
1. Open **[https://www.helius.dev](https://www.helius.dev)** in browser
2. Click **"Sign Up"** (or **"Get Started"**)
3. Create account (email + password)
4. On the dashboard, find your **API Key**
5. Copy it
   ```
   SAVE THIS: HELIUS_API_KEY
   Example: 1a2b3c4d5e6f7g8h9i0j
   ```

### 3b. DexScreener & RugCheck
- **DexScreener**: No signup needed, free API
- **RugCheck**: No signup needed, free API

---

## ✅ STEP 4: Create `.env` File (3 minutes)

### 4a. Open Terminal
Open your terminal and run:

```bash
cd /home/hermes/token-sniper
```

### 4b. Create `.env` File
Copy this and fill in YOUR values:

```bash
cat > .env << 'EOF'
# Discord
DISCORD_BOT_TOKEN=PASTE_YOUR_BOT_TOKEN_HERE
DISCORD_CHANNEL_ID=PASTE_YOUR_CHANNEL_ID_HERE
DISCORD_WEBHOOK_URL=

# Solana
HELIUS_API_KEY=PASTE_YOUR_HELIUS_API_KEY_HERE
HELIUS_WEBSOCKET_URL=wss://mainnet.helius-rpc.com/?api-key=PASTE_YOUR_HELIUS_API_KEY_HERE

# Thresholds (BALANCED profile - recommended)
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
EOF
```

**IMPORTANT:** Replace these with YOUR actual values:
- `PASTE_YOUR_BOT_TOKEN_HERE` → Your Discord bot token from Step 1b
- `PASTE_YOUR_CHANNEL_ID_HERE` → Your channel ID from Step 2b
- `PASTE_YOUR_HELIUS_API_KEY_HERE` → Your Helius API key from Step 3a

### 4c. Verify `.env` Created
```bash
cat .env
```

You should see your tokens/IDs filled in.

---

## ✅ STEP 5: Install Dependencies (2 minutes)

```bash
cd /home/hermes/token-sniper
pip install -r requirements.txt
```

Wait for it to finish. You'll see:
```
Successfully installed python-telegram-bot discord.py aiohttp requests python-dotenv solders websockets
```

---

## ✅ STEP 6: Run the Bot! (1 minute)

```bash
cd /home/hermes/token-sniper
python main.py
```

You should see output like:
```
✅ Config loaded: Discord=true, Telegram=false
✅ Discord bot ready as TokenSniper#1234
🤖 Token Sniper Bot starting...
ℹ️ Bot initialized and ready
⏳ Waiting for tokens... (running simulation demo)
📡 Simulating token detection: FROG
```

---

## 🎉 WHAT HAPPENS NEXT

The bot is now running in **demo/simulation mode**. It will:

1. **Simulate detecting a token** called "Frog Pump v2" (FROG)
2. **Send a test Discord alert** to your #token-sniper channel
3. **Show you what a real alert looks like**

### ✅ Check Your Discord Channel
Look in your `#token-sniper` channel. You should see a rich embed like:

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

---

## 🛑 TO STOP THE BOT

Press **CTRL + C** in your terminal

---

## 🎓 NEXT STEPS

### Immediate (Now)
- ✅ Run the bot and see the demo alert in Discord
- ✅ Verify everything is working

### Short-term (Tomorrow)
- [ ] Let the bot run for 24-48 hours to see real signals
- [ ] Evaluate signal quality
- [ ] Tune thresholds if needed

### Medium-term (This Week)
- [ ] Deploy continuously (background/cron/systemd)
- [ ] Validate signal profitability (backtest/paper trade)
- [ ] Add Hermes webhook for execution signals

### Long-term (This Month)
- [ ] Build trading bot integration
- [ ] Add analytics dashboard
- [ ] Deploy to production (Docker/cloud)

---

## 🔧 TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'discord'"
→ Run: `pip install -r requirements.txt` again

### "Bot doesn't appear in Discord"
→ Check you pasted the OAuth2 invite link correctly in browser

### "No alert in Discord channel"
→ Check DISCORD_CHANNEL_ID is correct in .env
→ Check bot has "Send Messages" permission in channel

### "Config error: TELEGRAM_BOT_TOKEN or DISCORD_BOT_TOKEN must be set"
→ Check .env file exists: `ls -la .env`
→ Check DISCORD_BOT_TOKEN is filled in: `grep DISCORD_BOT_TOKEN .env`

---

## 📚 REFERENCE

| File | Purpose |
|------|---------|
| `.env` | Your configuration (tokens, API keys, thresholds) |
| `main.py` | The bot itself |
| `config.py` | Loads .env and validates |
| `notifiers/discord_notifier.py` | Sends Discord alerts |
| `filters/safety_filter.py` | Checks for honeypots |
| `filters/momentum_filter.py` | Scores tokens 0-100 |

---

## ⚠️ IMPORTANT NOTES

1. **The bot is currently in DEMO mode** — it simulates token detection
   - When you're ready for real-time detection, we'll replace the simulation with real Helius WebSocket listener

2. **API Keys are secure** — they're stored in `.env` which is NOT committed to git
   - Never share your `.env` file
   - Never commit it to GitHub

3. **Sensitivity Presets**
   - BALANCED is what's in .env (recommended)
   - Can switch to AGGRESSIVE or CONSERVATIVE later

---

**Status:** You're ready! Follow the steps above and you'll have alerts in Discord in ~15 minutes. 🚀

---
