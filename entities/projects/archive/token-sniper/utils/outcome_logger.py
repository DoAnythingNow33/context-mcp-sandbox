"""
Layer 5 — Feedback loop.

Every alert (and, if enabled, every reject) is written to `outcomes.jsonl` with
the full set of filter values that produced the decision. Alerts are then added
to a persistent watchlist and their price is polled at +1h / +6h / +24h from
DexScreener (cheap, free). After a few days this file is what tells us which
layer actually predicts outcome — so thresholds stop being guesses.

State survives a process restart: the watchlist is a JSON file reloaded on
startup, so a restart mid-window still completes the pending polls.
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from detectors.dexscreener_client import get_token_snapshot

logger = logging.getLogger(__name__)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class OutcomeLogger:
    def __init__(
        self,
        dexscreener_api_url: str,
        outcome_log_path: str = "data/outcomes.jsonl",
        watchlist_path: str = "data/watchlist.json",
        poll_hours: Optional[List[int]] = None,
        log_rejects: bool = True,
        poll_interval_sec: int = 300,
    ):
        self.dexscreener_api_url = dexscreener_api_url
        self.outcome_log_path = outcome_log_path
        self.watchlist_path = watchlist_path
        self.poll_hours = poll_hours or [1, 6, 24]
        self.log_rejects = log_rejects
        self.poll_interval_sec = poll_interval_sec
        os.makedirs(os.path.dirname(outcome_log_path) or ".", exist_ok=True)
        self._watchlist: List[Dict[str, Any]] = self._load_watchlist()

    # --- persistence ---
    def _load_watchlist(self) -> List[Dict[str, Any]]:
        try:
            with open(self.watchlist_path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_watchlist(self) -> None:
        tmp = f"{self.watchlist_path}.tmp"
        with open(tmp, "w") as f:
            json.dump(self._watchlist, f, indent=2)
        os.replace(tmp, self.watchlist_path)

    def _append_jsonl(self, record: Dict[str, Any]) -> None:
        with open(self.outcome_log_path, "a") as f:
            f.write(json.dumps(record, default=str) + "\n")

    # --- public API ---
    def record_decision(
        self,
        mint: str,
        symbol: str,
        decision: str,  # "alert" | "reject"
        stage: str,       # which layer decided
        snapshot: Dict[str, Any],
        layer_details: Dict[str, Any],
    ) -> None:
        if decision == "reject" and not self.log_rejects:
            return
        record = {
            "ts": _utc_iso(),
            "mint": mint,
            "symbol": symbol,
            "decision": decision,
            "stage": stage,
            "entry_price_usd": snapshot.get("price_usd"),
            "entry_lp_usd": snapshot.get("lp_size_usd"),
            "entry_fdv_usd": snapshot.get("fdv_usd"),
            "dex_id": snapshot.get("dex_id"),
            "migrated": snapshot.get("migrated"),
            "buys_m5": snapshot.get("buys_m5"),
            "sells_m5": snapshot.get("sells_m5"),
            "volume_m5_usd": snapshot.get("volume_m5_usd"),
            "price_change_m5_pct": snapshot.get("price_change_percent_2min"),
            "layers": layer_details,
        }
        self._append_jsonl(record)

        if decision == "alert":
            now = time.time()
            self._watchlist.append(
                {
                    "mint": mint,
                    "symbol": symbol,
                    "alerted_ts": _utc_iso(),
                    "entry_price_usd": snapshot.get("price_usd"),
                    "entry_lp_usd": snapshot.get("lp_size_usd"),
                    "due": {str(h): now + h * 3600 for h in self.poll_hours},
                    "results": {},
                }
            )
            self._save_watchlist()

    # --- background polling ---
    async def watch_loop(self) -> None:
        logger.info(
            f"📈 Outcome watch loop started ({len(self._watchlist)} pending), "
            f"polling at +{self.poll_hours}h"
        )
        while True:
            try:
                await self._poll_due()
            except Exception as e:
                logger.warning(f"Outcome poll error: {e}")
            await asyncio.sleep(self.poll_interval_sec)

    async def _poll_due(self) -> None:
        now = time.time()
        changed = False
        still_pending: List[Dict[str, Any]] = []

        for entry in self._watchlist:
            due = entry.get("due", {})
            fired_any = False
            for hour_key, due_ts in list(due.items()):
                if hour_key in entry["results"] or now < due_ts:
                    continue
                snap = await get_token_snapshot(self.dexscreener_api_url, entry["mint"])
                price = (snap or {}).get("price_usd")
                lp = (snap or {}).get("lp_size_usd")
                entry_price = entry.get("entry_price_usd") or 0
                mult = (price / entry_price) if (price and entry_price) else None
                entry["results"][hour_key] = {
                    "ts": _utc_iso(),
                    "price_usd": price,
                    "lp_usd": lp,
                    "multiple": round(mult, 3) if mult else None,
                    "dead": bool(snap is None or (lp is not None and lp < 500)),
                }
                changed = True
                fired_any = True
                self._append_jsonl(
                    {
                        "ts": _utc_iso(),
                        "type": "outcome_poll",
                        "mint": entry["mint"],
                        "symbol": entry["symbol"],
                        "hours_after": int(hour_key),
                        **entry["results"][hour_key],
                    }
                )
                logger.info(
                    f"📈 {entry['symbol']} +{hour_key}h: "
                    f"{entry['results'][hour_key]['multiple']}x "
                    f"(lp ${lp or 0:,.0f})"
                )

            max_hour = max(int(h) for h in due) if due else 0
            if len(entry["results"]) >= len(due):
                changed = True  # completed -> drop
            else:
                still_pending.append(entry)
            _ = fired_any, max_hour

        if changed:
            self._watchlist = still_pending
            self._save_watchlist()
