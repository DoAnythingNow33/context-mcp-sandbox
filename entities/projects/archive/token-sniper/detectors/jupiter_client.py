"""
Jupiter Quote API client (free) — used as a honeypot / can-I-sell-at-all check.

At a $5 position, liquidity *depth* is a non-issue: $5 exits almost anything
that has a route at all. So this is not a slippage/depth test — it is a test of
whether a sell is *possible*:

  - no route back to SOL            -> honeypot / sell-disabled -> reject
  - a route exists but the implied round-trip loss is large  -> transfer tax
    or a sell-side tax trap -> reject

Round-trip loss is estimated by quoting a BUY (SOL -> token) and an immediate
SELL (token -> SOL) of the resulting amount, both at the given USD size, and
comparing SOL out vs SOL in. A clean token round-trips at roughly the pool fee
(~1%); a taxed / trap token bleeds far more.
"""

import logging
from typing import Any, Dict, Optional

import aiohttp

logger = logging.getLogger(__name__)

SOL_MINT = "So11111111111111111111111111111111111111112"
_LAMPORTS_PER_SOL = 1_000_000_000


async def _quote(api_url: str, input_mint: str, output_mint: str, amount: int) -> Optional[Dict[str, Any]]:
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": str(amount),
        "slippageBps": "1500",
        "swapMode": "ExactIn",
        "onlyDirectRoutes": "false",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                if resp.status != 200:
                    return None
                return await resp.json(content_type=None)
    except Exception as e:
        logger.warning(f"Jupiter quote error: {e}")
        return None


async def check_sellability(
    api_url: str,
    token_mint: str,
    position_usd: float,
    sol_price_usd: float,
) -> Dict[str, Any]:
    """
    Returns:
      {
        "has_route": bool,
        "roundtrip_loss_pct": float | None,   # None if buy leg failed
        "reason": str,
      }
    """
    if not sol_price_usd or sol_price_usd <= 0:
        sol_price_usd = 150.0  # conservative fallback; only sets the quote size

    sol_in_lamports = max(1, int((position_usd / sol_price_usd) * _LAMPORTS_PER_SOL))

    buy = await _quote(api_url, SOL_MINT, token_mint, sol_in_lamports)
    if not buy or not buy.get("outAmount"):
        return {"has_route": False, "roundtrip_loss_pct": None, "reason": "no buy route"}

    token_amount = int(buy["outAmount"])
    if token_amount <= 0:
        return {"has_route": False, "roundtrip_loss_pct": None, "reason": "buy quote returned zero"}

    sell = await _quote(api_url, token_mint, SOL_MINT, token_amount)
    if not sell or not sell.get("outAmount"):
        return {"has_route": False, "roundtrip_loss_pct": None, "reason": "no sell route (honeypot)"}

    sol_out_lamports = int(sell["outAmount"])
    loss_pct = (1 - (sol_out_lamports / sol_in_lamports)) * 100

    return {
        "has_route": True,
        "roundtrip_loss_pct": round(loss_pct, 1),
        "reason": "ok",
    }
