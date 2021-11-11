from pydantic import BaseModel


class Colours(BaseModel):
    """Colour codes."""

    blue = 0x0279FD
    bright_green = 0x01D277
    dark_green = 0x1F8B4C
    orange = 0xE67E22
    pink = 0xCF84E0
    purple = 0xB734EB
    red = 0xFF0000
    soft_green = 0x68C290
    soft_orange = 0xF9CB54
    soft_red = 0xCD6D6D
    yellow = 0xF8E500
    python_blue = 0x4B8BBE
    python_yellow = 0xFFD43B
    grass_green = 0x66FF00
    gold = 0xE6C200


class Emojis(BaseModel):
    """Emoji codes."""

    track_previous = "\u23EE"  # ⏮
    track_next = "\u23ED"  # ⏭
    arrow_left = "\u2B05"  # ⬅
    arrow_right = "\u27A1"  # ➡
    lock = "\U0001F512"  # 🔒


class Constants(BaseModel):
    """The app constants."""

    colours: Colours = Colours()
    emojis: Emojis = Emojis()

    low_latency: int = 200
    high_latency: int = 400


constants = Constants()
