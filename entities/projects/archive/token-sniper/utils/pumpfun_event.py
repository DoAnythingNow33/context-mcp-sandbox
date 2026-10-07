"""
Decode pump.fun's `CreateEvent` straight out of the websocket log notification.

pump.fun emits an Anchor self-CPI event as a `Program data: <base64>` log line
on every token creation. That line is already delivered in the `logsSubscribe`
push — so the new mint address can be read from it with zero follow-up RPC
calls (no getTransaction, no getMultipleAccounts). Verified against live
mainnet Create events 2026-08-30.

Borsh layout after the 8-byte Anchor event discriminator:
    string  name
    string  symbol
    string  uri
    pubkey  mint            <- what we want
    pubkey  bonding_curve
    pubkey  user
    (trailing fields vary and are not needed)
"""

import base64
import binascii
import logging
import struct
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# First 8 bytes of sha256("event:CreateEvent") — the Anchor event discriminator.
CREATE_EVENT_DISCRIMINATOR = bytes.fromhex("1b72a94ddeeb6376")

_PROGRAM_DATA_PREFIX = "Program data: "

_B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def _b58encode(raw: bytes) -> str:
    n = int.from_bytes(raw, "big")
    out = ""
    while n > 0:
        n, rem = divmod(n, 58)
        out = _B58_ALPHABET[rem] + out
    for byte in raw:
        if byte == 0:
            out = "1" + out
        else:
            break
    return out


def _read_borsh_string(buf: bytes, offset: int):
    length = struct.unpack_from("<I", buf, offset)[0]
    offset += 4
    text = buf[offset:offset + length].decode("utf-8", "replace")
    return text, offset + length


def _decode_create_event(raw: bytes) -> Optional[Dict[str, Any]]:
    if len(raw) < 8 or raw[:8] != CREATE_EVENT_DISCRIMINATOR:
        return None
    try:
        offset = 8
        name, offset = _read_borsh_string(raw, offset)
        symbol, offset = _read_borsh_string(raw, offset)
        uri, offset = _read_borsh_string(raw, offset)
        mint = _b58encode(raw[offset:offset + 32])
        bonding_curve = _b58encode(raw[offset + 32:offset + 64])
        user = _b58encode(raw[offset + 64:offset + 96])
    except (struct.error, IndexError) as e:
        logger.warning(f"Malformed pump.fun CreateEvent: {e}")
        return None

    if len(mint) < 32:
        return None

    return {
        "mint": mint,
        "bonding_curve": bonding_curve,
        "user": user,
        "name": name,
        "symbol": symbol,
        "uri": uri,
    }


def parse_create_event(logs) -> Optional[Dict[str, Any]]:
    """
    Scan a log-notification's `logs` list for the pump.fun CreateEvent and
    return {mint, bonding_curve, user, name, symbol, uri}, or None if this
    notification isn't a token creation.
    """
    for line in logs:
        if not line.startswith(_PROGRAM_DATA_PREFIX):
            continue
        try:
            raw = base64.b64decode(line[len(_PROGRAM_DATA_PREFIX):])
        except (ValueError, binascii.Error):
            continue
        event = _decode_create_event(raw)
        if event:
            return event
    return None
