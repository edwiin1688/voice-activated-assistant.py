"""Logging configuration module"""

import logging
import sys
from typing import Optional

LOG_FORMAT = "[%(levelname)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: str = "INFO", debug: bool = False) -> logging.Logger:
    logger = logging.getLogger("voice_assistant")

    log_level = logging.DEBUG if debug else getattr(logging, level.upper())

    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
        logger.addHandler(handler)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(f"voice_assistant.{name}" if name else "voice_assistant")
