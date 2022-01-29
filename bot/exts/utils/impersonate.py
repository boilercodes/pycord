import json
import logging
import re

import discord.utils
from aiohttp import ClientResponse
from discord import Embed, Message, TextChannel
from discord.commands import (ApplicationContext, Option, SlashCommandGroup,
                              permissions)
from discord.errors import NotFound
from discord.ext import commands

from bot.bot import Bot
from bot.core import constants, settings

log = logging.getLogger(__name__)


class Impersonate(commands.Cog):
    """Impersonate and talk as the bot."""

    def __init__(self, bot: Bot):
        self.bot = bot

    message = SlashCommandGroup(
        "msg", "Talk and send messages under the bot's name.",
        guild_ids=settings.dev_guild_ids,
    )

    async def fetch_message(self, guild_id: int, channel_id: int, msg_id: int) -> Message:
        """
        Fetch a message by its guild id, channel id and message id.

        `ctx.fetch_message` will only try to fetch the message in the channel
        the command was executed in so this is a replacement.
        """
        try:
            guild = discord.utils.get(self.bot.guilds, id=guild_id)
            channel = discord.utils.get(guild.text_channels, id=channel_id)

            # Try to fetch and return the message in the channel.
            return await channel.fetch_message(msg_id)
        except (AttributeError, NotFound):
            # `ClientResponse` is a required positional argument.
            raise NotFound(ClientResponse, f"Failed to fetch the message of id {msg_id}.")

    @message.command()
    @permissions.has_role(settings.roles.admin)
    async def send(
            self, ctx: ApplicationContext,
            channel: Option(TextChannel, "Choose a channel."),
            content: Option(
                str,
                "Can be either a message link (https://discohook.org/) or the message itself."
            )
    ) -> None:
        """Send a message in a specific channel."""
        # Check if `content` is a message id to avoid API calls.
        if re.match(r"https://discord.com/channels/\d{18}/\d{18}/\d{18}", content):
            _, guild_id, channel_id, msg_id = content.rsplit("/", 3)
            try:
                msg = await self.fetch_message(int(guild_id), int(channel_id), int(msg_id))
                files = [await attachement.to_file() for attachement in msg.attachments]
                log.debug(f'"{content}" successfully fetched')

                try:
                    msg_content = re.search(r"```json([\s\S]*)```", msg.content)
                    try:
                        msg_content = msg_content.group(1)
                    except AttributeError:
                        msg_content = msg.content

                    # Try to convert `content` to a dictionary representing a message.
                    msg_json = json.loads(msg_content)

                    embeds = [Embed.from_dict(embed) for embed in msg_json.get("embeds")]
                    log.debug(f'"{content}" is a serializable dictionary, sending to channel')

                    # Copy and send the message from `msg_json` to the channel.
                    sent_msg = await channel.send(
                        content=msg_json.get("content"),
                        embeds=embeds,
                        files=files
                    )
                except json.decoder.JSONDecodeError:
                    # Copy and send the message to the channel.
                    sent_msg = await channel.send(content=msg.content, embeds=msg.embeds, files=files)
            except NotFound:
                error = f":x: Failed to fetch the message link [{content}]({content})."
                log.debug(error)

                # Send a hidden response to the author.
                await ctx.respond(error, ephemeral=True)
                return
        else:
            # If the content is not a message id or a serializable json
            # object then directly send the content to the channel.
            log.debug(f'"{content}" is a string, sending to channel')
            sent_msg = await channel.send(content)

        # Create the message link.
        link = f"https://discord.com/channels/{ctx.guild.id}/{channel.id}/{sent_msg.id}"

        # Send a hidden confirmation to the author.
        embed = Embed(
            colour=constants.colours.bright_green,
            description=f"[Message]({link}) sent to <#{channel.id}>"
        )

        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot: Bot) -> None:
    """Load the `Impersonate` cog."""
    bot.add_cog(Impersonate(bot))
