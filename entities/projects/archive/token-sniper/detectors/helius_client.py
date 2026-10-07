"""
Helius client — the two enrichment reads v2 needs that DexScreener can't give.

1. Holder count via the DAS `getTokenAccounts` method. Unlike
   `getTokenLargestAccounts` (which rejects Token-2022, i.e. every pump.fun
   mint), DAS `getTokenAccounts` works for Token-2022. Distinct holders with a
   non-zero balance is v2's proxy for "real wallets" — a wash farm running a
   dozen wallets shows a dozen-ish holders however many thousand txns it faked.

2. Creator dump check — has the creator wallet (known for free from the
   CreateEvent) already offloaded its position? One DAS `getTokenAccounts`
   filtered to the creator's owner, compared against a "dev still holds" floor.

Both run only for tokens that already cleared the free pre-filter, aging,
Layer 1 and Layer 3 — a handful per hour, not per launch.
"""

import logging
from typing import Any, Dict, List, Optional

import aiohttp

logger = logging.getLogger(__name__)


async def _das(rpc_url: str, method: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    payload = {"jsonrpc": "2.0", "id": "das", "method": method, "params": params}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(rpc_url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    logger.warning(f"Helius {method} HTTP {resp.status}")
                    return None
                data = await resp.json(content_type=None)
    except Exception as e:
        logger.warning(f"Helius {method} error: {e}")
        return None
    if "error" in data:
        logger.warning(f"Helius {method} error: {data['error']}")
        return None
    return data.get("result")


async def get_holder_stats(
    rpc_url: str,
    mint: str,
    creator: Optional[str] = None,
    exclude: Optional[set] = None,
    max_pages: int = 8,
) -> Dict[str, Any]:
    """
    Enumerate token accounts for `mint` (paginated, capped at max_pages * 1000)
    and return holder + distribution stats. `exclude` is a set of owner
    addresses to drop before distribution analysis (the AMM pool / bonding
    curve), so the "top holder" reflects a real wallet, not the market.

      {
        "holder_count": int,            # distinct owners with balance > 0 (incl. pool)
        "counted_all": bool,            # False if we hit the page cap
        "creator_holds": bool | None,
        "top_holder_pct": float | None,       # largest, INCLUDING pool
        "non_pool_top_pct": float | None,     # largest real wallet, pool excluded
        "top_pcts": [float, ...],             # top 20 real-wallet pcts, desc
        "flatness_ratio": float | None,       # top_pcts[0] / top_pcts[9]; ~1 = airdrop, >3 = organic
      }
    """
    exclude = exclude or set()
    owners_balance: Dict[str, int] = {}
    cursor: Optional[str] = None
    counted_all = True

    for page in range(max_pages):
        params: Dict[str, Any] = {"mint": mint, "limit": 1000}
        if cursor:
            params["cursor"] = cursor
        result = await _das(rpc_url, "getTokenAccounts", params)
        if not result:
            break
        accounts: List[Dict[str, Any]] = result.get("token_accounts", []) or []
        for acc in accounts:
            bal = int(acc.get("amount") or 0)
            if bal <= 0:
                continue
            owner = acc.get("owner")
            if owner:
                owners_balance[owner] = owners_balance.get(owner, 0) + bal
        cursor = result.get("cursor")
        if not cursor or not accounts:
            break
        if page == max_pages - 1:
            counted_all = False

    total = sum(owners_balance.values())
    top_pct = None
    if total > 0 and owners_balance:
        top_pct = round(max(owners_balance.values()) / total * 100, 1)

    creator_holds: Optional[bool] = None
    if creator:
        creator_holds = owners_balance.get(creator, 0) > 0

    # distribution among real wallets (pool/curve excluded)
    real = sorted(
        (bal for owner, bal in owners_balance.items() if owner not in exclude),
        reverse=True,
    )
    top_pcts = [round(b / total * 100, 3) for b in real[:20]] if total > 0 else []
    non_pool_top_pct = top_pcts[0] if top_pcts else None
    flatness_ratio = None
    if len(top_pcts) >= 10 and top_pcts[9] > 0:
        flatness_ratio = round(top_pcts[0] / top_pcts[9], 2)

    return {
        "holder_count": len(owners_balance),
        "counted_all": counted_all,
        "creator_holds": creator_holds,
        "top_holder_pct": top_pct,
        "non_pool_top_pct": non_pool_top_pct,
        "top_pcts": top_pcts,
        "flatness_ratio": flatness_ratio,
    }
