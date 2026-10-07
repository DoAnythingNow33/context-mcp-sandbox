"""Live check: the 旺财 token that passed v2 but Phantom flags must now be
rejected by the Layer 3 distribution gate. Also runs a known-organic token
through to confirm it still passes."""
import asyncio, sys
from config import Config
from detectors.pumpfun_api import get_pumpfun_coin
from detectors.helius_client import get_holder_stats
from filters.spam_filter import SpamFilter

FLAGGED = "Ax3U1fBeGPJHDgQYuW5WcSFzPXzYGp2epjw6gXTqpump"
ORGANIC = "EVgwa5CHBVwk6sCTa4QJrVXYBKngZhYqh2a2ZGDApump"

async def run(mint, label):
    coin = await get_pumpfun_coin(Config.PUMPFUN_API_BASE, mint)
    pool = coin and coin.get("pool_address")
    bc = coin and coin.get("bonding_curve")
    creator = coin and coin.get("creator")
    rpc = f"https://mainnet.helius-rpc.com/?api-key={Config.HELIUS_API_KEY}"
    hs = await get_holder_stats(rpc, mint, creator=creator,
                                exclude={a for a in (pool, bc, creator) if a})
    print(f"\n[{label}] {mint[:8]}  pool={pool}")
    print(f"  holders={hs['holder_count']} counted_all={hs['counted_all']} "
          f"non_pool_top={hs['non_pool_top_pct']}% flatness={hs['flatness_ratio']}")
    print(f"  top_pcts={hs['top_pcts'][:12]}")
    sf = SpamFilter()
    ok, det = sf.check(coin.get("symbol", "?") if coin else "?",
                       {"score": 1, "score_normalised": 1, "risks": []}, hs)
    print(f"  Layer 3 -> passed={ok}  {det['checks_failed'] or 'OK'}")

async def main():
    await run(FLAGGED, "PHANTOM-FLAGGED")
    await run(ORGANIC, "ORGANIC")

asyncio.run(main())
