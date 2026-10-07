"""
Layer 2 — Wash-trade / fake-momentum filter.

v1 scored transaction *count* and buy *ratio* — both trivially inflated by a
volume bot, so a 98%-buys wash farm scored ~maximum. v2 inverts that:

Hard gates (any one fails -> reject, no score can rescue it):
  - sell-side flow too thin   : sells/total < MIN_SELL_RATIO  (>~95% buys = wash)
  - sell-side flow too heavy   : sells/total > MAX_SELL_RATIO  (net distribution)
  - volume/liquidity ratio     : m5 volume / LP > MAX_VOL_LIQ_RATIO (wash churn)
  - too few real wallets       : distinct holders < MIN_UNIQUE_HOLDERS
  - hard dump at eval          : price change < HARD_DUMP_PCT

Score (0-100, informational + final bar) is built only from things a bot can't
cheaply fake: distinct holder count, a *healthy* (not maximal) buy skew,
genuine price action, and real linked socials. Raw tx count and buy ratio are
no longer positive drivers.
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


class MomentumFilter:
    def __init__(
        self,
        min_score: int = 55,
        min_lp_usd: int = 10_000,
        min_sell_ratio: float = 0.15,
        max_sell_ratio: float = 0.60,
        max_vol_liq_ratio: float = 8.0,
        min_unique_holders: int = 30,
        hard_dump_pct: float = -20.0,
    ):
        self.min_score = min_score
        self.min_lp_usd = min_lp_usd
        self.min_sell_ratio = min_sell_ratio
        self.max_sell_ratio = max_sell_ratio
        self.max_vol_liq_ratio = max_vol_liq_ratio
        self.min_unique_holders = min_unique_holders
        self.hard_dump_pct = hard_dump_pct

    def evaluate(self, token_data: Dict[str, Any]) -> Tuple[bool, int, Dict[str, Any]]:
        d: Dict[str, Any] = {"layer": "momentum", "checks_failed": [], "breakdown": {}}

        buys = token_data.get("buys_m5", token_data.get("buyers_2min", 0)) or 0
        sells = token_data.get("sells_m5", 0) or 0
        total = buys + sells
        vol = token_data.get("volume_m5_usd", 0) or 0
        lp = token_data.get("lp_size_usd", 0) or 0
        price_change = token_data.get("price_change_percent_2min", 0) or 0
        holders = token_data.get("holder_count", 0) or 0
        holders_partial = token_data.get("holder_count_partial", False)

        sell_ratio = (sells / total) if total > 0 else 0.0
        vol_liq_ratio = (vol / lp) if lp > 0 else float("inf")

        d["sell_ratio"] = round(sell_ratio, 3)
        d["vol_liq_ratio"] = round(vol_liq_ratio, 2) if vol_liq_ratio != float("inf") else None
        d["holder_count"] = holders
        d["price_change_pct"] = price_change

        # --- hard gates ---
        if total == 0:
            d["checks_failed"].append("no m5 transactions")
        else:
            if sell_ratio < self.min_sell_ratio:
                d["checks_failed"].append(
                    f"sell-side {sell_ratio*100:.0f}% < {self.min_sell_ratio*100:.0f}% (wash / one-sided)"
                )
            if sell_ratio > self.max_sell_ratio:
                d["checks_failed"].append(
                    f"sell-side {sell_ratio*100:.0f}% > {self.max_sell_ratio*100:.0f}% (net distribution)"
                )

        if vol_liq_ratio > self.max_vol_liq_ratio:
            d["checks_failed"].append(
                f"volume/LP {d['vol_liq_ratio']} > {self.max_vol_liq_ratio} (wash churn)"
            )

        if holders < self.min_unique_holders:
            # a partial holder count that's already above the floor is fine;
            # only fail if the (possibly capped) count is genuinely below it
            d["checks_failed"].append(
                f"{holders} distinct holders < {self.min_unique_holders}"
                + (" (count is a lower bound)" if holders_partial else "")
            )

        if price_change < self.hard_dump_pct:
            d["checks_failed"].append(f"hard dump {price_change:+.0f}% < {self.hard_dump_pct:+.0f}%")

        # --- informational score (only fake-resistant signals) ---
        score = 0.0
        holder_pts = min(40, (holders / 120) * 40)
        score += holder_pts
        d["breakdown"]["holders"] = f"{holder_pts:.0f}/40 ({holders})"

        if self.min_sell_ratio <= sell_ratio <= 0.5:
            band_pts = 20 * (1 - abs(sell_ratio - 0.3) / 0.3)
        else:
            band_pts = 0
        band_pts = max(0.0, band_pts)
        score += band_pts
        d["breakdown"]["sell_balance"] = f"{band_pts:.0f}/20 ({sell_ratio*100:.0f}% sells)"

        if price_change > 10:
            price_pts = 20
        elif price_change > 0:
            price_pts = 12
        elif price_change > -10:
            price_pts = 5
        else:
            price_pts = 0
        score += price_pts
        d["breakdown"]["price"] = f"{price_pts}/20 ({price_change:+.1f}%)"

        social_pts = 0
        socials = []
        if token_data.get("has_twitter"):
            social_pts += 8
            socials.append("Twitter")
        if token_data.get("has_website"):
            social_pts += 7
            socials.append("Website")
        if token_data.get("has_telegram"):
            social_pts += 5
            socials.append("Telegram")
        score += social_pts
        d["breakdown"]["social"] = f"{social_pts}/20 ({', '.join(socials) or 'None'})"

        final_score = int(min(100, score))
        d["score"] = final_score

        gates_ok = not d["checks_failed"]
        passed = gates_ok and final_score >= self.min_score and lp >= self.min_lp_usd
        if gates_ok and final_score < self.min_score:
            d["checks_failed"].append(f"score {final_score} < {self.min_score}")
        if gates_ok and lp < self.min_lp_usd:
            d["checks_failed"].append(f"LP ${lp:,.0f} < ${self.min_lp_usd:,}")

        d["passed"] = passed
        logger.info(
            f"Layer 2 (momentum) {token_data.get('token_symbol', '?')}: "
            f"{'PASS' if passed else 'FAIL'} score={final_score} {d['checks_failed']}"
        )
        return passed, final_score, d
