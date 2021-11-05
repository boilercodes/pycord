import logging
from enum import Enum
from functools import partial
from typing import Iterable, Optional

from discord.commands import Option, OptionChoice, slash_command
from discord.commands.context import ApplicationContext, AutocompleteContext
from discord.errors import ExtensionAlreadyLoaded, ExtensionNotLoaded
from discord.ext import commands

from bot import exts
from bot.bot import Bot
from bot.core import settings
from bot.utils.extensions import EXTENSIONS, loaded_extensions

log = logging.getLogger(__name__)

UNLOAD_BLACKLIST = {f"{exts.__name__}.core.extensions"}
BASE_PATH_LEN = len(exts.__name__.split("."))


class Action(Enum):
    """Represents an action to perform on an extension."""

    # Need to be partial otherwise they are considered to be function definitions.
    LOAD = partial(Bot.load_extension)
    UNLOAD = partial(Bot.unload_extension)
    RELOAD = partial(Bot.reload_extension)


class Choices:
    """Manage extensions autocomplete choices."""

    def __init__(self, action: Action):
        self.action = action

    @property
    def extensions(self) -> Iterable[str]:
        """Return a list of extensions according to the action."""
        if self.action == Action.LOAD:
            return EXTENSIONS - set(loaded_extensions)
        elif self.action == Action.UNLOAD:
            return set(loaded_extensions) - UNLOAD_BLACKLIST

        return EXTENSIONS

    @staticmethod
    def format_extension(extension: str) -> str:
        """Transform an extension into a human readable format."""
        return extension.removeprefix(f"{exts.__name__}.")

    def callback(self, ctx: AutocompleteContext) -> Iterable[OptionChoice]:
        """Return a list of option choices for the autocomplete."""
        return [OptionChoice(self.format_extension(extension), extension)
                for extension in self.extensions]


class Extensions(commands.Cog):
    """Extension management commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(guild_ids=settings.dev_guild_ids)
    async def ext_load(
            self, ctx: ApplicationContext,
            extension: Option(
                str, "Choose an extension.",
                autocomplete=Choices(Action.LOAD).callback
            )
    ) -> None:
        """Load an extension given its name."""
        msg, error = await self.manage(Action.LOAD, extension)
        await ctx.respond(msg)

    @slash_command(guild_ids=settings.dev_guild_ids)
    async def ext_unload(
            self, ctx: ApplicationContext,
            extension: Option(
                str, "Choose an extension.",
                autocomplete=Choices(Action.UNLOAD).callback
            )
    ) -> None:
        """Unload an extension given its name."""
        msg, error = await self.manage(Action.UNLOAD, extension)
        await ctx.respond(msg)

    @slash_command(guild_ids=settings.dev_guild_ids)
    async def ext_reload(
            self, ctx: ApplicationContext,
            extension: Option(
                str, "Choose an extension.",
                autocomplete=Choices(Action.RELOAD).callback
            )
    ) -> None:
        """Reload an extension given its name."""
        msg, error = await self.manage(Action.RELOAD, extension)
        await ctx.respond(msg)

    async def manage(self, action: Action, ext: str) -> tuple[str, Optional[str]]:
        """Apply an action to an extension and return the status message and any error message."""
        verb = action.name.lower()
        error_msg = None

        try:
            action.value(self.bot, ext)
            await self.bot.sync_commands()
        except (ExtensionAlreadyLoaded, ExtensionNotLoaded):
            if action is Action.RELOAD:
                # When reloading, just load the extension if it was not loaded.
                return await self.manage(Action.LOAD, ext)

            msg = f":x: Extension `{ext}` is already {verb}ed."
            log.debug(msg[4:])
        except Exception as e:
            if hasattr(e, "original"):
                e = e.original

            log.exception(f"Extension '{ext}' failed to {verb}.")

            error_msg = f"{e.__class__.__name__}: {e}"
            msg = f":x: Failed to {verb} extension `{ext}`:\n```\n{error_msg}\n```"
        else:
            msg = f":ok_hand: Extension successfully {verb}ed: `{ext}`."
            log.debug(msg[10:])

        return msg, error_msg


def setup(bot: Bot) -> None:
    """Loads the Extensions cog."""
    bot.add_cog(Extensions(bot))
