"""
Layer 1 — Sellability / honeypot (free, deterministic).

Runs before the on-chain safety read and before momentum scoring. Kills the
"went up on paper then I couldn't sell" trap Dan actually hit:

  - pump.fun `hidden` / `nsfw`        -> hard reject
  - not yet migrated off the curve    -> hard reject (default; REJECT_PRE_MIGRATION)
  - no Jupiter sell route             -> hard reject (honeypot)
  - round-trip loss > cap             -> hard reject (sell-side tax / trap)
  - liquidity below a modest floor    -> hard reject (sanity, not depth)

Every check returns a reason string; the whole layer returns (passed, details).
"""

import logging
from typing import Any, Dict, Optional, Tuple

from detectors.jupiter_client import check_sellability
from detectors.pumpfun_api import get_pumpfun_coin

logger = logging.getLogger(__name__)


class SellabilityFilter:
    def __init__(
        self,
        jupiter_api_url: str,
        pumpfun_api_base: str,
        position_usd: float = 5.0,
        max_roundtrip_loss_pct: float = 15.0,
        min_lp_usd: int = 10_000,
        reject_pre_migration: bool = True,
    ):
        self.jupiter_api_url = jupiter_api_url
        self.pumpfun_api_base = pumpfun_api_base
        self.position_usd = position_usd
        self.max_roundtrip_loss_pct = max_roundtrip_loss_pct
        self.min_lp_usd = min_lp_usd
        self.reject_pre_migration = reject_pre_migration

    async def check(
        self, mint: str, snapshot: Dict[str, Any], sol_price_usd: float
    ) -> Tuple[bool, Dict[str, Any]]:
        details: Dict[str, Any] = {"layer": "sellability", "checks_failed": [], "checks_passed": []}

        # --- pump.fun platform record ---
        coin = await get_pumpfun_coin(self.pumpfun_api_base, mint)
        details["pumpfun_found"] = coin is not None
        if coin:
            details["pumpfun_hidden"] = coin["hidden"]
            details["pumpfun_nsfw"] = coin["nsfw"]
            details["pumpfun_migrated"] = coin["migrated"]
            details["pumpfun_reply_count"] = coin["reply_count"]
            details["creator"] = coin["creator"]
            details["pool_address"] = coin.get("pool_address")
            details["bonding_curve"] = coin.get("bonding_curve")
            details["pumpfun_twitter"] = coin["twitter"]
            details["pumpfun_verified"] = coin.get("verified")
            if coin.get("is_banned"):
                details["checks_failed"].append("pump.fun: token is banned")
            if coin["hidden"]:
                details["checks_failed"].append("pump.fun: token is hidden")
            if coin["nsfw"]:
                details["checks_failed"].append("pump.fun: token is nsfw-flagged")

        # --- migration status (DexScreener dexId, backed up by pump.fun `complete`) ---
        migrated = bool(snapshot.get("migrated")) or bool(coin and coin["migrated"])
        details["migrated"] = migrated
        if self.reject_pre_migration and not migrated:
            details["checks_failed"].append(
                f"pre-migration (on bonding curve, dexId={snapshot.get('dex_id') or '?'})"
            )

        # --- liquidity sanity floor ---
        lp = snapshot.get("lp_size_usd", 0) or 0
        details["lp_size_usd"] = lp
        if lp < self.min_lp_usd:
            details["checks_failed"].append(f"LP ${lp:,.0f} < ${self.min_lp_usd:,} floor")

        # --- Jupiter honeypot / sell-route check ---
        sell = await check_sellability(self.jupiter_api_url, mint, self.position_usd, sol_price_usd)
        details["has_sell_route"] = sell["has_route"]
        details["roundtrip_loss_pct"] = sell["roundtrip_loss_pct"]
        if not sell["has_route"]:
            details["checks_failed"].append(f"Jupiter: {sell['reason']}")
        elif sell["roundtrip_loss_pct"] is not None and sell["roundtrip_loss_pct"] > self.max_roundtrip_loss_pct:
            details["checks_failed"].append(
                f"round-trip loss {sell['roundtrip_loss_pct']}% > {self.max_roundtrip_loss_pct}% (sell tax / trap)"
            )

        passed = not details["checks_failed"]
        details["passed"] = passed
        logger.info(
            f"Layer 1 (sellability) {mint[:8]}: {'PASS' if passed else 'FAIL'} "
            f"{details['checks_failed']}"
        )
        return passed, details
