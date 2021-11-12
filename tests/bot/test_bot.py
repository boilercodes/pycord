import pytest

from bot.bot import Bot
from bot.utils.extensions import EXTENSIONS


class TestBot:
    """Test the `Bot` class."""

    @pytest.mark.asyncio
    async def test_http_session(self) -> None:
        """Test if the bot HTTP session works."""
        bot = Bot()

        # Make sure the HTTP session is running.
        assert not bot.http_session.closed

        # Make sure to close the bot.
        await bot.close()
        assert bot.http_session.closed

    @pytest.mark.asyncio
    async def test_add_cog(self) -> None:
        """Test if the bot HTTP session works."""
        bot = Bot()

        # Bot extensions must be empty.
        assert not bot.extensions

        # Load all cogs extensions.
        for ext in EXTENSIONS:
            bot.load_extension(ext)

        # All extensions should be loaded.
        assert len(bot.extensions) == len(EXTENSIONS)

        await bot.close()
