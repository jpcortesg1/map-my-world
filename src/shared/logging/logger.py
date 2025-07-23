"""Logger configuration for Map My World API."""
import sys
from typing import Any
from loguru import logger
from config.core import get_settings

settings = get_settings()

# Remove default logger
logger.remove()

# Add colored console logger
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.log_level,
    colorize=True,
    backtrace=True,
    diagnose=True,
)

# Add file logger for production
if not settings.debug:
    logger.add(
        "logs/app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )


def get_logger(name: str) -> Any:
    """Get logger instance for a module."""
    return logger.bind(name=name) 