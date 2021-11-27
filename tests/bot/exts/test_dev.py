"""This file should be removed if you plan on removing the dev commands."""

from bot.exts import dev


class TestDev:
    """Test the `Dev` cog."""

    def test_setup(self, bot):
        """Test the setup method of the cog."""
        # Invoke the command
        dev.setup(bot)

        bot.add_cog.assert_called_once()
