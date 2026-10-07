"""
pump.fun frontend API client (free, unofficial).

`frontend-api.pump.fun/coins/{mint}` returns the platform's own view of a
token: whether it has migrated off the bonding curve (`complete`), moderation
flags (`hidden`, `nsfw`), the reply/comment count, the creator wallet, and any
linked socials. All of that is useful to v2:

  - Layer 1 rejects `hidden` / `nsfw` outright and (by default) rejects
    tokens that have not yet migrated.
  - Layer 4 (later) uses `reply_count` + the linked Twitter as a free social
    proxy.

Unofficial endpoint — treat every field as optional and degrade gracefully.
"""

import logging
from typing import Any, Dict, Optional

import aiohttp

logger = logging.getLogger(__name__)

_HEADERS = {
    # the endpoint 403s a bare python-aiohttp UA
    "User-Agent": "Mozilla/5.0 (compatible; token-sniper/2.0)",
    "Accept": "application/json",
}


async def get_pumpfun_coin(api_base: str, mint: str) -> Optional[Dict[str, Any]]:
    """
    Fetch pump.fun's record for a mint. Returns a normalised dict or None if
    the endpoint is unreachable / returns nothing.
    """
    url = f"{api_base.rstrip('/')}/{mint}"
    try:
        async with aiohttp.ClientSession(headers=_HEADERS) as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                if resp.status != 200:
                    logger.info(f"pump.fun API HTTP {resp.status} for {mint[:8]}")
                    return None
                data = await resp.json(content_type=None)
    except Exception as e:
        logger.warning(f"pump.fun API error for {mint[:8]}: {e}")
        return None

    if not isinstance(data, dict) or not data.get("mint"):
        return None

    return {
        "migrated": bool(data.get("complete")),
        "hidden": bool(data.get("hidden")),
        "nsfw": bool(data.get("nsfw")),
        "reply_count": int(data.get("reply_count") or 0),
        "market_cap_usd": float(data.get("usd_market_cap") or 0.0),
        "creator": data.get("creator") or data.get("dev") or None,
        "twitter": data.get("twitter") or None,
        "telegram": data.get("telegram") or None,
        "website": data.get("website") or None,
        "verified": bool(data.get("verified")),
        "is_banned": bool(data.get("is_banned")),
        "ath_market_cap_usd": float(data.get("ath_market_cap") or 0.0),
        "bonding_curve": data.get("bonding_curve") or None,
        "pool_address": (
            data.get("pool_address")
            or data.get("pump_swap_pool")
            or data.get("raydium_pool")
            or None
        ),
        "name": data.get("name"),
        "symbol": data.get("symbol"),
        "_raw_keys": sorted(data.keys()),
    }
