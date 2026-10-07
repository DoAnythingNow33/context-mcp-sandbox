"""Shared Solana JSON-RPC helpers. The only on-chain read the bot makes is a
single getAccountInfo per token in the safety filter (post pre-filter)."""

import asyncio
import aiohttp
import base64
import struct
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

MINT_LAYOUT_MIN_LEN = 82  # legacy SPL Token Mint account size

# Cap on concurrent RPC requests from this process — a safety margin against
# rate limits if many tokens clear the pre-filter at once.
_RPC_SEMAPHORE = asyncio.Semaphore(5)


async def rpc_call(rpc_url: str, method: str, params: list) -> Optional[dict]:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    async with _RPC_SEMAPHORE:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    rpc_url, json=payload, timeout=aiohttp.ClientTimeout(total=8)
                ) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        logger.warning(f"RPC {method} HTTP {resp.status}: {text[:200]}")
                        return None
                    # content_type=None: rate-limit/error responses sometimes come
                    # back with a non-JSON content-type even when the body is JSON
                    # (or vice versa) — don't let a strict mimetype check turn a
                    # real, parseable error into a confusing crash.
                    data = await resp.json(content_type=None)
        except Exception as e:
            logger.warning(f"RPC {method} error: {e}")
            return None

    if "error" in data:
        logger.warning(f"RPC {method} returned error: {data['error']}")
        return None

    return data.get("result")


def _decode_mint_data(raw: bytes) -> Optional[Dict[str, Any]]:
    """
    Decode raw SPL Mint account bytes.
    Layout (legacy Token program, 82 bytes):
      0..4   mint_authority COption tag (u32)
      4..36  mint_authority Pubkey
      36..44 supply (u64 LE)
      44     decimals (u8)
      45     is_initialized (bool)
      46..50 freeze_authority COption tag (u32)
      50..82 freeze_authority Pubkey
    """
    if len(raw) < MINT_LAYOUT_MIN_LEN:
        return None

    mint_authority_tag = struct.unpack_from("<I", raw, 0)[0]
    supply = struct.unpack_from("<Q", raw, 36)[0]
    decimals = raw[44]
    freeze_authority_tag = struct.unpack_from("<I", raw, 46)[0]

    return {
        "mint_authority_revoked": mint_authority_tag == 0,
        "freeze_authority_revoked": freeze_authority_tag == 0,
        "supply": supply,
        "decimals": decimals,
    }


async def get_mint_account(
    rpc_url: str, token_address: str, commitment: str = "confirmed"
) -> Optional[Dict[str, Any]]:
    """
    Decode a single SPL Mint account via getAccountInfo. Real on-chain read.

    Default commitment is "confirmed" rather than the RPC default of
    "finalized" — for a mint that was just created seconds ago (the pump.fun
    detection use case), finalized commitment lags enough to make this
    silently return nothing on a fresh mint.
    """
    result = await rpc_call(
        rpc_url, "getAccountInfo", [token_address, {"encoding": "base64", "commitment": commitment}]
    )
    if not result:
        return None

    value = result.get("value")
    if not value or not value.get("data"):
        return None

    try:
        raw = base64.b64decode(value["data"][0])
    except Exception as e:
        logger.warning(f"Failed to decode mint account data: {e}")
        return None

    return _decode_mint_data(raw)
