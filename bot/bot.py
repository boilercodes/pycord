import logging
import socket
from abc import ABC

import discord
from aiohttp import AsyncResolver, ClientSession, TCPConnector
from discord import Cog

from bot.core import settings

log = logging.getLogger(__name__)


class Bot(discord.Bot, ABC):
    """Base bot class."""

    name = settings.client.name

    def __init__(self, **kwargs):
        """Initiate the client with slash commands."""
        super().__init__(**kwargs)
        self.http_session = ClientSession(
            connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET)
        )

    async def on_ready(self) -> None:
        """Triggered when the bot is ready."""
        log.info(f"Started bot as {self.user} (ID: {self.user.id})")

    async def close(self) -> None:
        """Triggered when the bot is closed."""
        await super().close()

        if self.http_session:
            await self.http_session.close()

    def add_cog(self, cog: Cog, *, override: bool = False) -> None:
        """Log whenever a cog is loaded."""
        super().add_cog(cog, override=override)
        log.debug(f"Cog loaded: {cog.qualified_name}")


bot = Bot()
