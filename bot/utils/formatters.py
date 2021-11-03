from bot.core import constants


def color_level(value: float, low: float, high: float) -> int:
    """Return the color intensity of a value."""
    if value < low:
        return constants.colours.bright_green
    elif value < high:
        return constants.colours.orange
    else:
        return constants.colours.red
