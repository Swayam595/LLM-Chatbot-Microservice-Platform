"""A simple configurable logger using loguru."""
import os
import sys
from loguru import logger

logger.remove()

logger.level("INFO", color="<green>")
logger.level("WARNING", color="<yellow>")
logger.level("ERROR", color="<red>")
logger.level("DEBUG", color="<cyan>")
logger.level("CRITICAL", color="<red><bold>")

logger_level = os.getenv("LOG_LEVEL", "INFO")

logger.add(
    sys.stderr,
    level=logger_level,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "<level>{level}</level> | "
        "<cyan>{name}:{line}</cyan> - "
        "<level>{message}</level>"
    ),
    enqueue=True,
    colorize=True,
)


def get_logger(service_name: str):
    """
    Returns a logger instance patched to include the service_name in every record.
    """
    return logger.patch(lambda record: record["extra"].update(service_name=service_name))