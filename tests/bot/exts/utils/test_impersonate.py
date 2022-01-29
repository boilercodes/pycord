import pytest
from discord.errors import NotFound

from bot.exts.utils import impersonate


class TestImpersonate:
    """Test the `Impersonate` cog."""

    @pytest.mark.asyncio
    async def test_fetch_message(self, bot, id):
        cog = impersonate.Impersonate(bot)

        # `id` is randomly generated so `fetch_message` should raise an error.
        with pytest.raises(NotFound):
            await cog.fetch_message(id, id, id)

    @pytest.mark.asyncio
    async def test_send(self, bot, ctx, text_channel, id):
        """Test the response of the `send` command."""
        cog = impersonate.Impersonate(bot)

        # Invoke the command with a message id.
        msg_link = f"https://discord.com/channels/{id}/{id}/{id}"
        await cog.send.callback(cog, ctx, text_channel, msg_link)

        args, kwargs = ctx.respond.call_args
        assert args[0]  # Command should respond with a message.
        assert kwargs["ephemeral"]  # Make sure the message is sent in ephemeral mode.

        # Invoke the command with a message.
        msg = "This is a random message beep boop."
        await cog.send.callback(cog, ctx, text_channel, msg)

        args, kwargs = text_channel.send.call_args
        content: str = args[0]  # Message should be sent to the text channel.

        assert content == msg

    def test_setup(self, bot):
        """Test the setup method of the cog."""
        # Invoke the command
        impersonate.setup(bot)

        bot.add_cog.assert_called_once()
