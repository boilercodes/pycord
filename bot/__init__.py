import logging.handlers
import os
from pathlib import Path

import aiohttp
import arrow
from aiohttp import TraceRequestEndParams

from bot.core import settings

# Set timestamp of when execution started.
start_time = arrow.utcnow()

# Set up file logging.
log_dir = Path(f"{__name__}/logs")
log_file = log_dir / f"{arrow.utcnow().strftime('%d-%m-%Y')}.log"
os.makedirs(log_dir, exist_ok=True)

# File handler rotates logs every 5 MB.
file_handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=5 * (2 ** 20), backupCount=10, encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)

# Console handler prints to terminal.
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)

# Format configuration.
fmt = "%(asctime)s - %(name)s %(levelname)s: %(message)s"
datefmt = "%H:%M:%S"

# Add colors for logging if available.
try:
    from colorlog import ColoredFormatter

    console_handler.setFormatter(
        ColoredFormatter(fmt=f"%(log_color)s{fmt}", datefmt=datefmt))
except ModuleNotFoundError:
    pass

# Remove old loggers, if any.
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

# Silence irrelevant loggers.
logging.getLogger("discord").setLevel(logging.INFO)
logging.getLogger("discord.gateway").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)

# Setup new logging configuration.
logging.basicConfig(
    format=fmt,
    datefmt=datefmt,
    level=logging.DEBUG,
    handlers=[console_handler, file_handler]
)


async def on_request_end(session, context, params: TraceRequestEndParams) -> None:
    """Log all HTTP requests."""
    resp = params.response

    # Format and send logging message.
    protocol = f"HTTP/{resp.version.major}.{resp.version.minor}"
    message = f'"{resp.method} - {protocol}" {resp.url} <{resp.status}>'
    logging.getLogger('aiohttp.client').debug(message)


# Configure aiohttp logging.
trace_config = aiohttp.TraceConfig()
trace_config.on_request_end.append(on_request_end)
