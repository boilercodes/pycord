from bot.bot import bot
from bot.core import settings
from bot.utils.extensions import walk_extensions

# Load all cogs extensions.
for ext in walk_extensions():
    bot.load_extension(ext)

bot.run(settings.client.token)
