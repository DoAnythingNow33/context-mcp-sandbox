"""
Token Sniper Bot — main orchestrator.

Live detection (pump.fun via Helius websocket) -> free pre-filter -> aging wait
-> the v2 filter stack, in cost order:

  Layer 1  sellability / honeypot   (pump.fun API + Jupiter + DexScreener)
  safety   mint/freeze authority     (one getAccountInfo + RugCheck)
  Layer 3  spam / rug heuristics     (reuses RugCheck, symbol-farm, creator)
  holders  one Helius DAS read       (feeds Layer 2 + Layer 3 creator check)
  Layer 2  wash / fake-momentum      (DexScreener + holder count)

Every decision (alert or reject) is written to the Layer 5 outcome log, and
alerts are price-polled at +1h/+6h/+24h so thresholds can be tuned on data.
"""

import asyncio
import logging

from config import Config
from filters.safety_filter import SafetyFilter
from filters.momentum_filter import MomentumFilter
from filters.sellability_filter import SellabilityFilter
from filters.spam_filter import SpamFilter
from notifiers.discord_notifier import DiscordNotifier
from detectors.pumpfun_detector import PumpFunDetector
from detectors.dexscreener_client import get_token_snapshot, get_sol_price_usd
from detectors.helius_client import get_holder_stats
from utils.outcome_logger import OutcomeLogger

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TokenSniperBot:
    def __init__(self):
        Config.validate()

        self.sellability_filter = SellabilityFilter(
            jupiter_api_url=Config.JUPITER_QUOTE_API_URL,
            pumpfun_api_base=Config.PUMPFUN_API_BASE,
            position_usd=Config.POSITION_SIZE_USD,
            max_roundtrip_loss_pct=Config.L1_MAX_ROUNDTRIP_LOSS_PCT,
            min_lp_usd=Config.L1_MIN_LP_USD,
            reject_pre_migration=Config.REJECT_PRE_MIGRATION,
        )

        self.safety_filter = SafetyFilter(
            Config.RUGCHECK_API_URL,
            helius_api_key=Config.HELIUS_API_KEY,
            solana_rpc_url=Config.SOLANA_RPC_URL,
            rugcheck_max_score=Config.RUGCHECK_MAX_SCORE,
            ignored_risks=Config.SAFETY_IGNORED_RISKS,
        )

        self.spam_filter = SpamFilter(
            rugcheck_max_score=Config.RUGCHECK_MAX_SCORE,
            rugcheck_max_normalised=Config.RUGCHECK_MAX_NORMALISED,
            symbol_farm_window_sec=Config.SYMBOL_FARM_WINDOW_SEC,
            symbol_farm_max_repeats=Config.SYMBOL_FARM_MAX_REPEATS,
            airdrop_min_holders_for_check=Config.AIRDROP_MIN_HOLDERS_FOR_CHECK,
            airdrop_min_top_holder_pct=Config.AIRDROP_MIN_TOP_HOLDER_PCT,
            airdrop_min_flatness_ratio=Config.AIRDROP_MIN_FLATNESS_RATIO,
        )

        self.momentum_filter = MomentumFilter(
            min_score=Config.MOMENTUM_SCORE_THRESHOLD,
            min_lp_usd=Config.MIN_LP_USD,
            min_sell_ratio=Config.L2_MIN_SELL_RATIO,
            max_sell_ratio=Config.L2_MAX_SELL_RATIO,
            max_vol_liq_ratio=Config.L2_MAX_VOL_LIQ_RATIO,
            min_unique_holders=Config.L2_MIN_UNIQUE_HOLDERS,
            hard_dump_pct=Config.L2_HARD_DUMP_PCT,
        )

        self.outcomes = OutcomeLogger(
            dexscreener_api_url=Config.DEXSCREENER_API_URL,
            outcome_log_path=Config.OUTCOME_LOG_PATH,
            watchlist_path=Config.WATCHLIST_PATH,
            log_rejects=Config.OUTCOME_LOG_REJECTS,
        )

        self.discord = DiscordNotifier(
            bot_token=Config.DISCORD_BOT_TOKEN,
            channel_id=Config.DISCORD_CHANNEL_ID,
            webhook_url=Config.DISCORD_WEBHOOK_URL,
            blocked_channel_id=Config.DISCORD_BLOCKED_CHANNEL_ID
        ) if Config.DISCORD_BOT_TOKEN else None

        self.detector = PumpFunDetector(websocket_url=Config.HELIUS_WEBSOCKET_URL)

        self.detected_tokens = set()
        self.alerted_tokens = set()
        self._eval_tasks = set()

    async def initialize(self):
        logger.info("🤖 Token Sniper Bot (v2) starting...")
        if self.discord:
            await self.discord.initialize()
            await self.discord.send_alert(
                "🤖 Token Sniper Bot online — **v2 filter stack**.\n"
                f"Pre-filter: {Config.PREFILTER_MIN_BUYERS}+ buys / "
                f"${Config.PREFILTER_MIN_LP_USD:,}+ LP at +{Config.PREFILTER_WAIT_SEC}s. "
                f"Full eval at +{Config.EVAL_DELAY_SEC // 60}min:\n"
                "• L1 sellability: migrated-only, has Jupiter sell route, "
                f"round-trip loss ≤{Config.L1_MAX_ROUNDTRIP_LOSS_PCT:.0f}%, not hidden/nsfw\n"
                "• safety: mint/freeze authority revoked\n"
                f"• L3 spam: RugCheck hard-fail, no ticker farm, creator still holding\n"
                f"• L2 wash: sell-side {Config.L2_MIN_SELL_RATIO*100:.0f}–{Config.L2_MAX_SELL_RATIO*100:.0f}%, "
                f"vol/LP ≤{Config.L2_MAX_VOL_LIQ_RATIO:.0f}, ≥{Config.L2_MIN_UNIQUE_HOLDERS} holders, "
                f"no hard dump, score ≥{Config.MOMENTUM_SCORE_THRESHOLD}\n"
                "Every decision logged; alerts price-polled at +1/6/24h.",
                level="info"
            )
        logger.info("✅ Bot initialized and ready")

    async def handle_new_mint(self, token_address: str, event: dict):
        if token_address in self.detected_tokens:
            return
        self.detected_tokens.add(token_address)
        task = asyncio.create_task(self._evaluate_token(token_address, event))
        self._eval_tasks.add(task)
        task.add_done_callback(self._eval_tasks.discard)

    def _log(self, mint, symbol, decision, stage, snapshot, layers):
        try:
            self.outcomes.record_decision(mint, symbol, decision, stage, snapshot or {}, layers)
        except Exception as e:
            logger.warning(f"outcome log failed: {e}")

    async def _evaluate_token(self, token_address: str, event: dict):
        sym = event.get("symbol", "?")
        logger.info(f"📍 Detected new token: {token_address[:8]}... ({sym})")

        # Stage 1: free pre-filter — drop the dead-on-arrival majority.
        await asyncio.sleep(Config.PREFILTER_WAIT_SEC)
        snapshot = await get_token_snapshot(Config.DEXSCREENER_API_URL, token_address)
        if not snapshot:
            logger.info(f"⏭️  {token_address[:8]}... no DexScreener data at +{Config.PREFILTER_WAIT_SEC}s — dropped")
            return
        if (
            snapshot.get("buyers_2min", 0) < Config.PREFILTER_MIN_BUYERS
            or snapshot.get("lp_size_usd", 0) < Config.PREFILTER_MIN_LP_USD
        ):
            logger.info(
                f"⏭️  {token_address[:8]}... failed pre-filter "
                f"(buys={snapshot.get('buyers_2min', 0)}, lp=${snapshot.get('lp_size_usd', 0):,.0f})"
            )
            return

        # Stage 2: age the token before judging it.
        remaining_wait = max(0, Config.EVAL_DELAY_SEC - Config.PREFILTER_WAIT_SEC)
        if remaining_wait:
            logger.info(
                f"👀 {token_address[:8]}... cleared pre-filter — aging {remaining_wait}s"
            )
            await asyncio.sleep(remaining_wait)

        # Fresh snapshot for evaluation.
        snapshot = await get_token_snapshot(Config.DEXSCREENER_API_URL, token_address) or snapshot
        snapshot["token_address"] = token_address
        snapshot["token_symbol"] = snapshot.get("symbol") or sym
        snapshot["token_name"] = snapshot.get("name") or event.get("name", "Unknown")
        sol_price = await get_sol_price_usd(Config.DEXSCREENER_API_URL)

        layers: dict = {}

        # --- Layer 1: sellability / honeypot ---
        l1_ok, l1 = await self.sellability_filter.check(token_address, snapshot, sol_price)
        layers["sellability"] = l1
        creator = l1.get("creator")
        pool_address = l1.get("pool_address")
        if not l1_ok:
            self._log(token_address, sym, "reject", "sellability", snapshot, layers)
            return

        # --- safety: mint/freeze authority (one on-chain read) ---
        is_safe, safety = await self.safety_filter.check_token_safety(token_address)
        layers["safety"] = {k: safety.get(k) for k in (
            "score", "checks_failed", "mint_authority_revoked",
            "freeze_authority_revoked", "lp_locked", "rugcheck_score",
        )}
        if not is_safe:
            logger.warning(f"🔴 {token_address[:8]}... safety fail: {safety['checks_failed']}")
            self._log(token_address, sym, "reject", "safety", snapshot, layers)
            if self.discord and Config.ALERT_ON_HIGH_MOMENTUM:
                await self.discord.send_blocking_reason(
                    token_address,
                    f"Safety: {safety['checks_failed'][0] if safety['checks_failed'] else 'unknown'}",
                    {"Score": f"{safety['score']}/100"},
                )
            return

        # --- one Helius DAS read: holder stats (feeds Layer 3 + Layer 2) ---
        holder_stats = {}
        if Config.HELIUS_API_KEY:
            rpc = f"https://mainnet.helius-rpc.com/?api-key={Config.HELIUS_API_KEY}"
            exclude = {a for a in (pool_address, creator, l1.get("bonding_curve")) if a}
            holder_stats = await get_holder_stats(
                rpc, token_address, creator=creator, exclude=exclude
            )
        layers["holders"] = holder_stats
        snapshot["holder_count"] = holder_stats.get("holder_count", 0)
        snapshot["holder_count_partial"] = not holder_stats.get("counted_all", True)

        # --- Layer 3: spam / rug ---
        l3_ok, l3 = self.spam_filter.check(
            symbol=sym,
            rugcheck=safety.get("rugcheck"),
            holder_stats=holder_stats,
        )
        layers["spam"] = l3
        if not l3_ok:
            self._log(token_address, sym, "reject", "spam", snapshot, layers)
            return

        # --- Layer 2: wash / fake-momentum ---
        l2_ok, score, l2 = self.momentum_filter.evaluate(snapshot)
        layers["momentum"] = l2
        snapshot["momentum_score"] = score
        if not l2_ok:
            self._log(token_address, sym, "reject", "momentum", snapshot, layers)
            return

        # --- passed everything ---
        logger.info(f"🚀 SIGNAL: {sym} (score {score}) — sending alert")
        snapshot.update({k: safety.get(k) for k in (
            "mint_authority_revoked", "freeze_authority_revoked", "lp_locked", "rugcheck_score",
        )})
        self._log(token_address, sym, "alert", "passed", snapshot, layers)
        if self.discord:
            await self.discord.send_signal_embed(snapshot)
        self.alerted_tokens.add(token_address)

    async def run(self):
        await self.initialize()
        logger.info("👂 Listening for new pump.fun launches on Solana mainnet...")
        watch_task = asyncio.create_task(self.outcomes.watch_loop())
        try:
            await self.detector.listen(self.handle_new_mint)
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped")
        finally:
            watch_task.cancel()
            if self.discord:
                await self.discord.close()


async def main():
    bot = TokenSniperBot()
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
