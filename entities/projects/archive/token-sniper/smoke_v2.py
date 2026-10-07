"""Live $0 smoke test for the v2 external APIs. Not part of the bot."""
import asyncio, sys
from detectors.dexscreener_client import get_token_snapshot, get_sol_price_usd
from detectors.pumpfun_api import get_pumpfun_coin
from detectors.jupiter_client import check_sellability
from detectors.helius_client import get_holder_stats
from config import Config

# a known migrated pump.fun token (USELESS) — swap if it 404s
MINT = sys.argv[1] if len(sys.argv) > 1 else "Dz9mQ9NzkBcCsuGPFJ3rXTHR5Mpv6oPjaZQ9V4h2b2yh"

async def main():
    sol = await get_sol_price_usd(Config.DEXSCREENER_API_URL)
    print(f"SOL price: {sol}")
    snap = await get_token_snapshot(Config.DEXSCREENER_API_URL, MINT)
    print(f"DexScreener: dex_id={snap and snap.get('dex_id')} migrated={snap and snap.get('migrated')} "
          f"lp={snap and snap.get('lp_size_usd')} buys={snap and snap.get('buys_m5')} sells={snap and snap.get('sells_m5')} "
          f"vol={snap and snap.get('volume_m5_usd')}")
    coin = await get_pumpfun_coin(Config.PUMPFUN_API_BASE, MINT)
    print(f"pump.fun: {coin if not coin else {k: coin[k] for k in ('migrated','hidden','nsfw','reply_count','creator','twitter')}}")
    sell = await check_sellability(Config.JUPITER_QUOTE_API_URL, MINT, 5.0, sol)
    print(f"Jupiter sellability: {sell}")
    if Config.HELIUS_API_KEY:
        rpc = f"https://mainnet.helius-rpc.com/?api-key={Config.HELIUS_API_KEY}"
        hs = await get_holder_stats(rpc, MINT, creator=coin and coin.get("creator"))
        print(f"Helius holders: {hs}")
    else:
        print("Helius: no key")

asyncio.run(main())
