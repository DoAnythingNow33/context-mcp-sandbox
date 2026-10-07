"""
DexScreener API client — fetches a real trading/liquidity snapshot for a token.

Known limitation: DexScreener's finest bucket is 5 minutes ("m5") — there is
no true 2-minute window available from this API. For tokens that are only a
couple of minutes old (the bot's actual use case, since we snapshot shortly
after a fresh pump.fun launch), the m5 bucket largely overlaps the token's
whole trading history so far, making it a reasonable proxy — but it is not
literally "the last 2 minutes," and slightly over-counts for anything a bit
older. Flagged here rather than silently mislabeled as precise.

Also: "buyers_2min" below is actually a BUY-TRANSACTION count, not a unique-
wallet count — DexScreener's public API doesn't expose unique wallet counts.
Kept under that field name only because momentum_filter.py already expects
it; treat it as an activity proxy, not literally "N distinct people bought."
"""

import aiohttp
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


async def get_token_snapshot(dexscreener_api_url: str, token_address: str) -> Optional[Dict[str, Any]]:
    url = f"{dexscreener_api_url}/tokens/{token_address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
    except Exception as e:
        logger.warning(f"DexScreener error for {token_address}: {e}")
        return None

    pairs = [p for p in (data.get("pairs") or []) if p.get("chainId") == "solana"]
    if not pairs:
        return None

    # Pick the pair with the most USD liquidity — the "real" market for this token
    pair = max(pairs, key=lambda p: (p.get("liquidity") or {}).get("usd", 0) or 0)

    txns_m5 = (pair.get("txns") or {}).get("m5") or {}
    volume_m5 = (pair.get("volume") or {}).get("m5", 0) or 0
    price_change_m5 = (pair.get("priceChange") or {}).get("m5", 0) or 0
    liquidity_usd = (pair.get("liquidity") or {}).get("usd", 0) or 0

    buys = txns_m5.get("buys", 0) or 0
    sells = txns_m5.get("sells", 0) or 0
    total = buys + sells

    info = pair.get("info") or {}
    socials = info.get("socials") or []
    websites = info.get("websites") or []

    dex_id = (pair.get("dexId") or "").lower()
    # pump.fun bonding-curve pairs surface as dexId "pumpfun". Anything else
    # (pumpswap / raydium / meteora / orca) means the token has migrated to a
    # real AMM.
    migrated = bool(dex_id) and dex_id != "pumpfun"

    return {
        "name": (pair.get("baseToken") or {}).get("name", "Unknown"),
        "symbol": (pair.get("baseToken") or {}).get("symbol", "?"),
        "lp_size_usd": liquidity_usd,
        "buys_m5": buys,
        "sells_m5": sells,
        "buyers_2min": buys,  # legacy field name kept for callers; = m5 buy-tx count
        "transactions_2min": total,
        "volume_m5_usd": volume_m5,
        "price_change_percent_2min": price_change_m5,
        "price_usd": float(pair.get("priceUsd") or 0) or 0.0,
        "fdv_usd": float(pair.get("fdv") or 0) or 0.0,
        "dex_id": dex_id,
        "migrated": migrated,
        "pair_created_at": pair.get("pairCreatedAt"),
        "has_twitter": any(s.get("type") == "twitter" for s in socials),
        "has_website": len(websites) > 0,
        "has_telegram": any(s.get("type") == "telegram" for s in socials),
        "twitter_url": next((s.get("url") for s in socials if s.get("type") == "twitter"), None),
        "website_url": websites[0].get("url") if websites else None,
        "chart_url": pair.get("url"),
        "sources": ["helius", "dexscreener"],
    }


async def get_sol_price_usd(dexscreener_api_url: str) -> float:
    """Best-effort SOL/USD from DexScreener. Falls back to 150.0 on any error —
    only used to size Jupiter quote amounts, so approximate is fine."""
    wsol = "So11111111111111111111111111111111111111112"
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{dexscreener_api_url}/tokens/{wsol}"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                if resp.status != 200:
                    return 150.0
                data = await resp.json()
        pairs = [p for p in (data.get("pairs") or []) if p.get("chainId") == "solana"]
        # keep only deep stablecoin-quoted pairs — those price WSOL itself
        stables = {"USDC", "USDT"}
        prices = sorted(
            float(p["priceUsd"])
            for p in pairs
            if p.get("priceUsd")
            and (p.get("quoteToken") or {}).get("symbol") in stables
            and (p.get("liquidity") or {}).get("usd", 0) > 100_000
            and 20 < float(p["priceUsd"]) < 2000
        )
        return prices[len(prices) // 2] if prices else 150.0
    except Exception:
        return 150.0
