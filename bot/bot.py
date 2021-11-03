import logging

import discord

from bot.core import settings

log = logging.getLogger(__name__)


class Bot(discord.Bot):
    """Base bot class."""

    name = settings.client.name

    def __init__(self, **kwargs):
        """Initiate the client with slash commands."""
        super().__init__(**kwargs)

    async def on_ready(self) -> None:
        """Triggered when the bot is ready."""
        log.info(f"Started bot as {self.user} (ID: {self.user.id})")


bot = Bot()
