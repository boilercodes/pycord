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

    debug: bool = False

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"


settings = Global()
