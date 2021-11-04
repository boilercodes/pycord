from typing import List

from pydantic import BaseSettings


class Client(BaseSettings):
    """The API settings."""

    name: str = "Bot"
    token: str

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "BOT_"


class Global(BaseSettings):
    """The app settings."""

    client: Client = Client()
    guild_ids: List[int]
    dev_guild_ids: List[int]

    debug: bool = False

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        fields = {
            "dev_guild_ids": {
                "env": ["DEV_GUILD_IDS", "GUILD_IDS"]
            }
        }


settings = Global()
