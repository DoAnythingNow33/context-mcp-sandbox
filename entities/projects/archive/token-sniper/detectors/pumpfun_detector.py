"""
Pump.fun new-token detector.

Subscribes to Solana mainnet via a websocket RPC endpoint using the plain
`logsSubscribe` method (universally supported), filtered to pump.fun's program.
On each token creation, the new mint is decoded directly from the `Program
data:` event log carried in the notification itself — see utils.pumpfun_event.
No getTransaction / getMultipleAccounts follow-up is made, so detection costs
zero RPC credits; the first (and only) on-chain read for a token happens later
in the safety filter, and only for tokens that already cleared the free
pre-filter.
"""

import asyncio
import json
import logging
from typing import Callable, Awaitable, Dict, Any, Set

import websockets

from utils.pumpfun_event import parse_create_event

logger = logging.getLogger(__name__)

PUMPFUN_PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

# Called with (mint_address, event_info) where event_info is the decoded
# CreateEvent (mint, bonding_curve, user, name, symbol, uri).
OnNewMint = Callable[[str, Dict[str, Any]], Awaitable[None]]


class PumpFunDetector:
    def __init__(self, websocket_url: str, rpc_url: str = ""):
        self.websocket_url = websocket_url
        self.rpc_url = rpc_url  # unused now; kept for call-site compatibility
        self._seen_signatures: Set[str] = set()

    async def listen(self, on_new_mint: OnNewMint):
        """Connect and listen forever, reconnecting on any drop."""
        if not self.websocket_url:
            logger.error("No HELIUS_WEBSOCKET_URL configured — cannot listen for new tokens.")
            return

        backoff = 5
        while True:
            try:
                await self._listen_once(on_new_mint)
                backoff = 5  # reset after a clean run
            except Exception as e:
                logger.warning(f"Pump.fun websocket dropped ({e}), reconnecting in {backoff}s")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 60)

    async def _listen_once(self, on_new_mint: OnNewMint):
        async with websockets.connect(self.websocket_url, ping_interval=20) as ws:
            sub = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "logsSubscribe",
                "params": [{"mentions": [PUMPFUN_PROGRAM_ID]}, {"commitment": "confirmed"}],
            }
            await ws.send(json.dumps(sub))
            ack = await ws.recv()
            logger.info(f"Pump.fun log subscription ack: {ack}")

            async for message in ws:
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    continue

                result = data.get("params", {}).get("result")
                if not result:
                    continue

                value = result.get("value", {})
                logs = value.get("logs", [])
                signature = value.get("signature")

                if not signature or signature in self._seen_signatures:
                    continue

                # Every pump.fun notification carries its event logs; only
                # token-creation notifications decode as a CreateEvent. Trades
                # and account-creations return None and are skipped for free.
                event = parse_create_event(logs)
                if not event:
                    continue

                self._seen_signatures.add(signature)
                if len(self._seen_signatures) > 5000:
                    self._seen_signatures = set(list(self._seen_signatures)[-2500:])

                logger.info(f"📍 Resolved new pump.fun mint {event['mint']} from tx {signature[:12]}...")
                await on_new_mint(event["mint"], event)
