import logging

import arrow
from dateutil.relativedelta import relativedelta
from discord import Embed
from discord.commands import ApplicationContext, slash_command
from discord.ext import commands

from bot import start_time
from bot.bot import Bot
from bot.core import settings
from bot.utils.formatters import color_level

log = logging.getLogger(__name__)


class Ping(commands.Cog):
    """Get info about the bot's ping and uptime."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(guild_ids=settings.guild_ids)
    async def ping(self, ctx: ApplicationContext) -> None:
        """Ping the bot to see its latency and uptime."""
        difference = relativedelta(arrow.utcnow() - start_time)
        uptime: str = start_time.shift(
            seconds=-difference.seconds,
            minutes=-difference.minutes,
            hours=-difference.hours,
            days=-difference.days
        ).humanize()

        latency = round(self.bot.latency * 1000)

        embed = Embed(
            colour=color_level(latency),
            description=f"• Gateway Latency: **{latency}ms**\n• Start time: **{uptime}**"
        )

        await ctx.respond(embed=embed)


def setup(bot: Bot) -> None:
    """Load the `Ping` cog."""
    bot.add_cog(Ping(bot))
