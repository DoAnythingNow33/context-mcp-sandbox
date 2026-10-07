"""
Configuration loader for Token Sniper Bot.
Reads from environment variables (.env file).
"""

import os
from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    try:
        return int(raw) if raw else default
    except ValueError:
        return default


def _float(name: str, default: float) -> float:
    raw = os.getenv(name, "").strip()
    try:
        return float(raw) if raw else default
    except ValueError:
        return default


def _bool(name: str, default: bool) -> bool:
    raw = os.getenv(name, "").strip().lower()
    if not raw:
        return default
    return raw in ("1", "true", "yes", "on")


def _opt_id(name: str):
    raw = os.getenv(name, "").strip()
    return int(raw) if raw.isdigit() and int(raw) != 0 else None


class Config:
    # Discord
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
    DISCORD_CHANNEL_ID = _opt_id("DISCORD_CHANNEL_ID")
    DISCORD_BLOCKED_CHANNEL_ID = _opt_id("DISCORD_BLOCKED_CHANNEL_ID")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

    # Solana RPC & APIs
    HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", "")
    HELIUS_WEBSOCKET_URL = os.getenv("HELIUS_WEBSOCKET_URL", "")
    SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

    DEXSCREENER_API_URL = "https://api.dexscreener.com/latest/dex"
    RUGCHECK_API_URL = "https://api.rugcheck.xyz/v1/tokens"
    JUPITER_QUOTE_API_URL = os.getenv("JUPITER_QUOTE_API_URL", "https://lite-api.jup.ag/swap/v1/quote")
    PUMPFUN_API_BASE = os.getenv("PUMPFUN_API_BASE", "https://frontend-api-v3.pump.fun/coins")

    # ---- v2 filters ----
    # Locked decision (2026-08-31): $5 position, so depth is a non-issue; the
    # sell-sim is a honeypot check, and the high-value levers are wash + social.
    POSITION_SIZE_USD = _float("POSITION_SIZE_USD", 5.0)

    # Layer 1 — sellability / honeypot
    L1_MAX_ROUNDTRIP_LOSS_PCT = _float("L1_MAX_ROUNDTRIP_LOSS_PCT", 15.0)
    L1_MIN_LP_USD = _int("L1_MIN_LP_USD", 10_000)
    REJECT_PRE_MIGRATION = _bool("REJECT_PRE_MIGRATION", True)

    # Layer 2 — wash / fake-momentum (provisional; tune against Layer 5 data)
    L2_MIN_SELL_RATIO = _float("L2_MIN_SELL_RATIO", 0.15)
    L2_MAX_SELL_RATIO = _float("L2_MAX_SELL_RATIO", 0.60)
    L2_MAX_VOL_LIQ_RATIO = _float("L2_MAX_VOL_LIQ_RATIO", 8.0)
    L2_MIN_UNIQUE_HOLDERS = _int("L2_MIN_UNIQUE_HOLDERS", 30)
    L2_HARD_DUMP_PCT = _float("L2_HARD_DUMP_PCT", -20.0)

    # Layer 3 — spam / rug
    RUGCHECK_MAX_NORMALISED = _int("RUGCHECK_MAX_NORMALISED", 50)
    SYMBOL_FARM_WINDOW_SEC = _int("SYMBOL_FARM_WINDOW_SEC", 21_600)
    SYMBOL_FARM_MAX_REPEATS = _int("SYMBOL_FARM_MAX_REPEATS", 3)
    # dust / Sybil-airdrop distribution gate — the pattern Phantom labels "spam"
    AIRDROP_MIN_HOLDERS_FOR_CHECK = _int("AIRDROP_MIN_HOLDERS_FOR_CHECK", 300)
    AIRDROP_MIN_TOP_HOLDER_PCT = _float("AIRDROP_MIN_TOP_HOLDER_PCT", 1.2)
    AIRDROP_MIN_FLATNESS_RATIO = _float("AIRDROP_MIN_FLATNESS_RATIO", 2.5)

    # Layer 5 — outcome logging
    OUTCOME_LOG_PATH = os.getenv("OUTCOME_LOG_PATH", "data/outcomes.jsonl")
    WATCHLIST_PATH = os.getenv("WATCHLIST_PATH", "data/watchlist.json")
    OUTCOME_LOG_REJECTS = _bool("OUTCOME_LOG_REJECTS", True)

    # Final alert bar
    MIN_LP_USD = _int("MIN_LP_USD", 10_000)
    MIN_BUYERS_2MIN = _int("MIN_BUYERS_2MIN", 20)
    # v2 momentum score is built from fake-resistant signals only (holders,
    # sell balance, price, socials) — different scale from v1, lower bar.
    MOMENTUM_SCORE_THRESHOLD = _int("MOMENTUM_SCORE_THRESHOLD", 55)

    # Seconds after mint to run safety + momentum. Deliberately long: a fresh
    # pump.fun token always trips holder-concentration risks and has thin data;
    # judging it at ~30-60min gives a far more honest read.
    EVAL_DELAY_SEC = _int("EVAL_DELAY_SEC", 1800)

    # Cheap pre-filter (free DexScreener check), run before the aging wait, to
    # drop the dead-on-arrival majority so they aren't tracked for 30min.
    PREFILTER_WAIT_SEC = _int("PREFILTER_WAIT_SEC", 300)
    PREFILTER_MIN_BUYERS = _int("PREFILTER_MIN_BUYERS", 5)
    PREFILTER_MIN_LP_USD = _int("PREFILTER_MIN_LP_USD", 2000)

    # Safety filter tuning
    RUGCHECK_MAX_SCORE = _int("RUGCHECK_MAX_SCORE", 500)
    # Comma-separated RugCheck "danger" risk names to NOT treat as a hard
    # fail (case-insensitive substring match). Use to accept concentration
    # risks that are unavoidable for a token seconds old, e.g.:
    #   SAFETY_IGNORED_RISKS=top 10 holders,single holder,high ownership
    SAFETY_IGNORED_RISKS = [
        r.strip() for r in os.getenv("SAFETY_IGNORED_RISKS", "").split(",") if r.strip()
    ]

    # Alerts
    ALERT_ON_HIGH_MOMENTUM = os.getenv("ALERT_ON_HIGH_MOMENTUM", "true").lower() == "true"

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @staticmethod
    def validate():
        if not Config.DISCORD_BOT_TOKEN:
            raise ValueError("DISCORD_BOT_TOKEN must be set")
        if not Config.HELIUS_WEBSOCKET_URL:
            raise ValueError("HELIUS_WEBSOCKET_URL must be set — the bot can't detect launches without it")
        if not Config.HELIUS_API_KEY:
            print("⚠️  HELIUS_API_KEY not set — safety checks will use the public RPC (slow, rate-limited).")
        print(f"✅ Config loaded (Discord bot, pre-filter {Config.PREFILTER_WAIT_SEC}s, momentum bar {Config.MOMENTUM_SCORE_THRESHOLD})")


if __name__ == "__main__":
    Config.validate()
    print("Configuration ready.")
