"""
Discord Notifier - Send token alerts to Discord channel(s)

Passing signals (safety + momentum cleared) go to `channel_id`. Blocked
tokens and general bot-status messages go to `blocked_channel_id` (falls
back to `channel_id` if not configured), so the "signal" channel can be
mentioned/unmuted while the "blocked" channel gets muted.
"""

import discord
from discord.ext import commands
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime, timezone
import aiohttp


def _now():
    return datetime.now(timezone.utc)

class DiscordNotifier:
    """Handles Discord notifications for token signals"""

    def __init__(
        self,
        bot_token: str,
        channel_id: int = None,
        webhook_url: str = None,
        blocked_channel_id: int = None,
    ):
        """
        Initialize Discord notifier

        Args:
            bot_token: Discord bot token
            channel_id: Discord channel ID for passing-signal alerts
            webhook_url: Discord webhook URL for embeds (simpler, no bot needed)
            blocked_channel_id: Discord channel ID for blocked/status messages.
                Falls back to channel_id if not set.
        """
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.blocked_channel_id = blocked_channel_id or channel_id
        self.webhook_url = webhook_url
        self.bot = None
        self.session = None

    async def initialize(self):
        """Initialize Discord bot connection"""
        if self.webhook_url:
            # Webhook mode - no bot needed (posts to a single channel only)
            self.session = aiohttp.ClientSession()
            return

        # Bot mode
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix="!", intents=intents)

        @self.bot.event
        async def on_ready():
            print(f"✅ Discord bot ready as {self.bot.user}")

        # Start bot in background
        asyncio.create_task(self.bot.start(self.bot_token))
        await asyncio.sleep(2)  # Wait for connection

    async def _send_embed(self, embed: "discord.Embed", channel_id: Optional[int]):
        """Dispatch a built embed via webhook (if configured) or bot to a specific channel."""
        if self.webhook_url:
            async with aiohttp.ClientSession() as session:
                await session.post(self.webhook_url, json={"embeds": [embed.to_dict()]})
        elif self.bot and channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.send(embed=embed)

    async def send_signal_embed(self, token_data: Dict[str, Any]):
        """
        Send a formatted token signal to the passing-signal channel.

        Args:
            token_data: Token metadata and signal info
        """
        embed = discord.Embed(
            title=f"🚀 {token_data.get('token_name', 'Unknown')} ({token_data.get('token_symbol', '?')})",
            description="Passed safety checks and cleared your momentum threshold — not investment advice, verify before acting.",
            color=discord.Color.green(),
            timestamp=_now()
        )

        embed.add_field(
            name="📊 Key Metrics",
            value=f"""
            **Momentum Score:** {token_data.get('momentum_score', 0)}/100
            **LP Size:** ${token_data.get('lp_size_usd', 0):,.0f}
            **Buy txns (~5m):** {token_data.get('buyers_2min', 0)}
            **Price change (~5m):** {token_data.get('price_change_percent_2min', 0):+.1f}%
            """,
            inline=False
        )

        embed.add_field(
            name="✅ Safety Checks",
            value=f"""
            Mint Authority Revoked: {token_data.get('mint_authority_revoked', False)}
            Freeze Authority Revoked: {token_data.get('freeze_authority_revoked', False)}
            LP Locked: {token_data.get('lp_locked', False)}
            RugCheck Score: {token_data.get('rugcheck_score', 'N/A')}
            """,
            inline=False
        )

        embed.add_field(
            name="📍 Token Address",
            value=f"`{token_data.get('token_address', 'N/A')}`",
            inline=False
        )

        links = []
        if token_data.get('twitter_url'):
            links.append(f"[Twitter]({token_data['twitter_url']})")
        if token_data.get('website_url'):
            links.append(f"[Website]({token_data['website_url']})")
        if token_data.get('chart_url'):
            links.append(f"[Chart]({token_data['chart_url']})")

        if links:
            embed.add_field(name="🔗 Links", value=" | ".join(links), inline=False)

        embed.set_footer(text=f"Sources: {', '.join(token_data.get('sources', []))}")

        await self._send_embed(embed, self.channel_id)

    async def send_alert(self, message: str, level: str = "info"):
        """
        Send a simple text status alert — goes to the blocked/general channel
        so the passing-signal channel stays alert-only.
        """
        color_map = {
            "info": discord.Color.blue(),
            "warning": discord.Color.orange(),
            "error": discord.Color.red()
        }
        emoji_map = {"info": "ℹ️", "warning": "⚠️", "error": "❌"}

        embed = discord.Embed(
            title=f"{emoji_map.get(level, 'ℹ️')} {level.upper()}",
            description=message,
            color=color_map.get(level, discord.Color.blue()),
            timestamp=_now()
        )

        await self._send_embed(embed, self.blocked_channel_id)

    async def send_blocking_reason(self, token_address: str, reason: str, details: Dict[str, Any] = None):
        """Send why a token was blocked — goes to the blocked/general channel."""
        embed = discord.Embed(
            title="🔴 Token Blocked",
            description=reason,
            color=discord.Color.red(),
            timestamp=_now()
        )

        embed.add_field(name="Token Address", value=f"`{token_address}`", inline=False)

        if details:
            for key, value in details.items():
                embed.add_field(name=key, value=str(value), inline=True)

        await self._send_embed(embed, self.blocked_channel_id)

    async def close(self):
        """Clean up connections"""
        if self.session:
            await self.session.close()
            self.session = None
        if self.bot:
            await self.bot.close()
