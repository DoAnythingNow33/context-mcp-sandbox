"""
Safety Filter — detect honeypots, rugs, and unsafe tokens.

Uses RugCheck API + a direct on-chain read of mint/freeze authority (via
utils.solana_rpc). LP-lock status is inferred from RugCheck's own risk feed
rather than independently verified on-chain — see _infer_lp_lock.

Hard fails (token is rejected regardless of any score):
  - mint authority still open       (can infinite-mint / dilute)
  - freeze authority still open      (can freeze holders out)
  - mint account can't be read on-chain (don't alert on an unknown)
  - any RugCheck "danger" risk whose name isn't in ignored_risks

Top-holder concentration via getTokenLargestAccounts is NOT checked: Helius
rejects Token-2022-owned mints ("not a Token mint"), and pump.fun tokens are
always Token-2022 — every call would fail and burn a credit for nothing.
"""

from typing import Dict, Any, Tuple, Optional, List
import logging

import aiohttp

from utils.solana_rpc import get_mint_account

logger = logging.getLogger(__name__)


class SafetyFilter:
    """Multi-check safety filter for token screening."""

    def __init__(
        self,
        rugcheck_api_url: str,
        helius_api_key: str = "",
        solana_rpc_url: str = "https://api.mainnet-beta.solana.com",
        rugcheck_max_score: int = 500,
        ignored_risks: Optional[List[str]] = None,
    ):
        self.rugcheck_api_url = rugcheck_api_url
        self.helius_api_key = helius_api_key
        self.solana_rpc_url = solana_rpc_url
        self.rugcheck_max_score = rugcheck_max_score
        # RugCheck risk names (case-insensitive substring match) that should
        # NOT count as a hard fail — e.g. holder-concentration risks that are
        # unavoidable artifacts of a token being seconds old. Empty by default.
        self.ignored_risks = [r.strip().lower() for r in (ignored_risks or []) if r.strip()]

    def rpc_url(self) -> str:
        if self.helius_api_key:
            return f"https://mainnet.helius-rpc.com/?api-key={self.helius_api_key}"
        return self.solana_rpc_url

    def _risk_ignored(self, name: str) -> bool:
        low = name.lower()
        return any(pat in low for pat in self.ignored_risks)

    async def check_token_safety(self, token_address: str) -> Tuple[bool, Dict[str, Any]]:
        """Run the full safety check. Returns (is_safe, details)."""
        details: Dict[str, Any] = {
            "token_address": token_address,
            "checks_passed": [],
            "checks_failed": [],
            "score": 100,
        }
        hard_fail = False

        # Check 1: RugCheck report
        rugcheck_result = await self._check_rugcheck(token_address)
        if rugcheck_result:
            rc_score = rugcheck_result.get("score", 0)
            details["rugcheck_score"] = rc_score
            # expose the parsed report for Layer 3 (spam filter) so it isn't
            # fetched twice
            details["rugcheck"] = {
                "score": rc_score,
                "score_normalised": rugcheck_result.get("score_normalised"),
                "risks": rugcheck_result.get("risks", []),
            }

            if rc_score > self.rugcheck_max_score:
                details["checks_failed"].append(f"RugCheck: risk score {rc_score} > {self.rugcheck_max_score}")
                details["score"] -= 50
            else:
                details["checks_passed"].append("RugCheck score OK")

            for risk in rugcheck_result.get("risks", []):
                name = str(risk.get("name", "Unknown"))
                if risk.get("level") == "danger":
                    if self._risk_ignored(name):
                        details["checks_passed"].append(f"RugCheck danger ignored by config: {name}")
                        continue
                    details["checks_failed"].append(f"RugCheck danger: {name}")
                    details["score"] -= 20
                    hard_fail = True
        else:
            details["checks_failed"].append("RugCheck: report unavailable")
            details["score"] -= 10

        # Checks 2 & 3: mint + freeze authority — real on-chain read
        mint_account = await get_mint_account(self.rpc_url(), token_address)

        if mint_account is None:
            details["checks_failed"].append("Could not read mint account on-chain")
            details["mint_authority_revoked"] = None
            details["freeze_authority_revoked"] = None
            details["score"] -= 15
            hard_fail = True  # don't alert on a token we couldn't verify
        else:
            if mint_account["mint_authority_revoked"]:
                details["checks_passed"].append("Mint authority revoked")
                details["mint_authority_revoked"] = True
            else:
                details["checks_failed"].append("Mint authority is open")
                details["mint_authority_revoked"] = False
                details["score"] -= 40
                hard_fail = True

            if mint_account["freeze_authority_revoked"]:
                details["checks_passed"].append("Freeze authority revoked")
                details["freeze_authority_revoked"] = True
            else:
                details["checks_failed"].append("Freeze authority is open")
                details["freeze_authority_revoked"] = False
                details["score"] -= 40
                hard_fail = True

        # Check 4: LP lock — inferred from RugCheck's risk feed, not verified
        # on-chain. Soft signal only (deducts score, never a hard fail).
        lp_info = self._infer_lp_lock(rugcheck_result)
        if lp_info is None:
            details["checks_failed"].append("LP lock status unknown (no RugCheck data)")
            details["lp_locked"] = False
            details["score"] -= 10
        elif lp_info["is_locked"]:
            details["checks_passed"].append("LP tokens locked (via RugCheck)")
            details["lp_locked"] = True
        else:
            details["checks_failed"].append("LP tokens not locked/burned (via RugCheck)")
            details["lp_locked"] = False
            details["score"] -= 20

        details["score"] = max(0, details["score"])

        is_safe = (not hard_fail) and details["score"] >= 40

        logger.info(
            f"Safety check for {token_address}: {'PASS' if is_safe else 'FAIL'} "
            f"(score {details['score']}, hard_fail={hard_fail})"
        )
        return is_safe, details

    async def _check_rugcheck(self, token_address: str) -> Optional[Dict[str, Any]]:
        try:
            url = f"{self.rugcheck_api_url}/{token_address}/report"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception as e:
            logger.warning(f"RugCheck API error: {e}")
        return None

    def _infer_lp_lock(self, rugcheck_result: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Best-effort LP lock status inferred from RugCheck's risk list rather
        than verified on-chain (real detection needs per-AMM pool parsing —
        Raydium / Meteora / pump.fun bonding curve all differ).
        """
        if not rugcheck_result:
            return None
        risks = rugcheck_result.get("risks", [])
        lp_risk_found = any(
            "liquidity" in str(r.get("name", "")).lower() or "lp" in str(r.get("name", "")).lower()
            for r in risks
        )
        return {"is_locked": not lp_risk_found}
