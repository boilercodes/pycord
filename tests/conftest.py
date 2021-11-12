import os


def pytest_configure() -> None:
    """Configure required variables for the bot."""
    # This is a fake randomly generated token.
    os.environ['BOT_TOKEN'] = "ODk3MTVyNDO0MDAxODE0NTC4.YWRgYg.hqWNRy2vEoc8feoNqR0ubBCYwxo"
    os.environ['GUILD_IDS'] = "[776477173123907605,831216309592653835]"
