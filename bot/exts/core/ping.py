import logging

from discord import ApplicationContext, Embed
from discord.commands import slash_command
from discord.ext import commands

from bot.bot import Bot
from bot.core import constants

log = logging.getLogger(__name__)


class Ping(commands.Cog):
    """Get info about the bot's ping and uptime."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(guild_ids=[855528466333564971], name="ping")
    async def ping(self, ctx: ApplicationContext) -> None:
        """Ping the bot to see its latency and state."""
        embed = Embed(
            title=":ping_pong: Pong!",
            colour=constants.colours.bright_green,
            description=f"Gateway Latency: {round(self.bot.latency * 1000)}ms",
        )

        await ctx.respond(embed=embed)


def setup(bot: Bot) -> None:
    """Loads the Ping cog."""
    bot.add_cog(Ping(bot))
