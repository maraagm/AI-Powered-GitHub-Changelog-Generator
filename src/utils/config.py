"""Configuration and environment variable utilities."""

import os
import sys
from datetime import datetime, timezone


def get_env(name: str, required: bool = True) -> str | None:
    """
    Read an environment variable, optionally raising an error if missing.

    Args:
        name: Environment variable name.
        required: If True, exit with an error message when the variable is absent.

    Returns:
        The variable value, or None if not set and not required.
    """
    value = os.getenv(name)
    if required and not value:
        print(f"Error: Required environment variable '{name}' is not set.", file=sys.stderr)
        sys.exit(1)
    return value


def utc_now_iso() -> str:
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(tz=timezone.utc).isoformat()


def truncate(text: str, max_length: int = 500) -> str:
    """
    Truncate a string to a maximum length, appending '...' when truncated.

    Args:
        text: Text to truncate.
        max_length: Maximum number of characters.

    Returns:
        Truncated string.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
