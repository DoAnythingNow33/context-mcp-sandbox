"""
Layer 3 — Spam / rug heuristics (free, high signal).

  - RugCheck score over cap            -> HARD fail (v1 treated this as soft -50)
  - RugCheck normalised score over cap  -> HARD fail
  - symbol relaunched many times in a rolling window -> ticker farm -> reject
  - dust / Sybil-airdrop holder distribution -> reject (this is what Phantom's
    own spam classifier catches, and RugCheck does not — see below)

Airdrop distribution check: a token mass-distributed to thousands of wallets to
fake a holder base shows a dead-flat distribution among real (non-pool) wallets
— every top holder within a hair of every other, largest real wallet well
under 1% of supply. An organic token decays as a power law (top wallet several
%, then a long tail). We flag flat + dust distributions because that is exactly
the pattern Phantom labels "spam", making the token painful to actually buy.
Needs the pool address excluded first (from the pump.fun API).

`creator_holds` is recorded for the Layer 5 feedback log but is NOT a gate: a
pump.fun creator receives no tokens by default, so "holds zero" is the normal
state, not a rug signal.

The symbol-farm tracker is in-process only (the bot is one long-running
process). It records every symbol that reaches this layer with a timestamp and
rejects a symbol that shows up more than `max_repeats` times inside `window_sec`.

Phantom / Blowfish blocklist lookup is intentionally NOT wired yet: there is no
confirmed free, unauthenticated endpoint for it. Left as a documented Phase-2
add rather than a fake check. See v2 plan, Layer 3.
"""

import logging
import time
from collections import defaultdict, deque
from typing import Any, Deque, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class SymbolFarmTracker:
    def __init__(self, window_sec: int, max_repeats: int):
        self.window_sec = window_sec
        self.max_repeats = max_repeats
        self._seen: Dict[str, Deque[float]] = defaultdict(deque)

    def record_and_check(self, symbol: str, now: Optional[float] = None) -> Tuple[bool, int]:
        """Record this sighting, prune old ones, return (is_farm, count_in_window)."""
        now = now if now is not None else time.time()
        key = (symbol or "?").strip().upper()
        dq = self._seen[key]
        dq.append(now)
        cutoff = now - self.window_sec
        while dq and dq[0] < cutoff:
            dq.popleft()
        return len(dq) > self.max_repeats, len(dq)


class SpamFilter:
    def __init__(
        self,
        rugcheck_max_score: int = 500,
        rugcheck_max_normalised: int = 50,
        symbol_farm_window_sec: int = 21_600,
        symbol_farm_max_repeats: int = 3,
        airdrop_min_holders_for_check: int = 300,
        airdrop_min_top_holder_pct: float = 1.2,
        airdrop_min_flatness_ratio: float = 2.5,
    ):
        self.rugcheck_max_score = rugcheck_max_score
        self.rugcheck_max_normalised = rugcheck_max_normalised
        self.symbol_tracker = SymbolFarmTracker(symbol_farm_window_sec, symbol_farm_max_repeats)
        self.airdrop_min_holders_for_check = airdrop_min_holders_for_check
        self.airdrop_min_top_holder_pct = airdrop_min_top_holder_pct
        self.airdrop_min_flatness_ratio = airdrop_min_flatness_ratio

    def check(
        self,
        symbol: str,
        rugcheck: Optional[Dict[str, Any]],
        holder_stats: Optional[Dict[str, Any]],
        now: Optional[float] = None,
    ) -> Tuple[bool, Dict[str, Any]]:
        details: Dict[str, Any] = {"layer": "spam", "checks_failed": [], "checks_passed": []}

        # --- RugCheck score, now a hard fail ---
        if rugcheck:
            raw = rugcheck.get("score")
            norm = rugcheck.get("score_normalised")
            details["rugcheck_score"] = raw
            details["rugcheck_score_normalised"] = norm
            if raw is not None and raw > self.rugcheck_max_score:
                details["checks_failed"].append(f"RugCheck score {raw} > {self.rugcheck_max_score}")
            if norm is not None and norm > self.rugcheck_max_normalised:
                details["checks_failed"].append(
                    f"RugCheck normalised {norm} > {self.rugcheck_max_normalised}"
                )
        else:
            details["checks_failed"].append("RugCheck report unavailable")

        # --- symbol / ticker farm ---
        is_farm, count = self.symbol_tracker.record_and_check(symbol, now)
        details["symbol_seen_in_window"] = count
        if is_farm:
            details["checks_failed"].append(
                f"ticker farm: '{symbol}' seen {count}x in window"
            )

        # --- dust / Sybil-airdrop distribution (the Phantom-spam pattern) ---
        hs = holder_stats or {}
        holder_count = hs.get("holder_count", 0) or 0
        non_pool_top = hs.get("non_pool_top_pct")
        flatness = hs.get("flatness_ratio")
        details["non_pool_top_pct"] = non_pool_top
        details["flatness_ratio"] = flatness
        details["top_pcts"] = hs.get("top_pcts")
        if holder_count >= self.airdrop_min_holders_for_check and non_pool_top is not None:
            if non_pool_top < self.airdrop_min_top_holder_pct:
                details["checks_failed"].append(
                    f"dust distribution: largest real wallet {non_pool_top:.2f}% "
                    f"of supply across {holder_count} holders (airdrop / Phantom-spam pattern)"
                )
            if flatness is not None and flatness < self.airdrop_min_flatness_ratio:
                details["checks_failed"].append(
                    f"flat holder distribution: top/10th ratio {flatness} "
                    f"< {self.airdrop_min_flatness_ratio} (manufactured holder base)"
                )

        # --- creator hold status: logged only, not a gate (see module docstring) ---
        details["creator_holds"] = hs.get("creator_holds")
        details["top_holder_pct"] = hs.get("top_holder_pct")

        passed = not details["checks_failed"]
        details["passed"] = passed
        logger.info(f"Layer 3 (spam) {symbol}: {'PASS' if passed else 'FAIL'} {details['checks_failed']}")
        return passed, details
