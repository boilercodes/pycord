import logging

from discord.commands import ApplicationContext, slash_command
from discord.ext import commands

from bot import settings
from bot.bot import Bot

log = logging.getLogger(__name__)


class Dev(commands.Cog):
    """Test different commands and pycord features."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(guild_ids=settings.dev_guild_ids)
    async def test(self, ctx: ApplicationContext) -> None:
        """Usage for testing purposes."""
        await ctx.defer()


def setup(bot: Bot) -> None:
    """Load the `Dev` cog."""
    bot.add_cog(Dev(bot))
