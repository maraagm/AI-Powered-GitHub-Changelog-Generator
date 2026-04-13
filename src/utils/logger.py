"""Centralized logging configuration for the changelog generator."""

import logging
import os

_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(level=_LOG_LEVEL, format=_FORMAT, datefmt=_DATE_FORMAT)


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger for the given module name.

    Args:
        name: Usually ``__name__`` of the calling module.

    Returns:
        Configured :class:`logging.Logger` instance.
    """
    return logging.getLogger(name)
