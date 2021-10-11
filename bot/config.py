from os import environ


class Settings:
    debug = environ.get("DEBUG", "").lower() == "true"


class Client:
    name = "Bot"
    token = environ.get("BOT_TOKEN")
