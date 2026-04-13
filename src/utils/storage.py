"""Persistent storage for tracking the last processed pull request."""

import json
import os

from src.utils.logger import get_logger

logger = get_logger(__name__)

_DEFAULT_PATH = "output/.last_pr.json"


def save_last_pr(pr_number: int, storage_path: str = _DEFAULT_PATH) -> None:
    """
    Persist the number of the last processed pull request.

    Args:
        pr_number: The pull request number to save.
        storage_path: Path to the JSON file used for storage.
    """
    os.makedirs(os.path.dirname(storage_path) or ".", exist_ok=True)
    with open(storage_path, "w", encoding="utf-8") as fh:
        json.dump({"last_pr": pr_number}, fh)
    logger.debug("Saved last processed PR #%s to %s", pr_number, storage_path)


def load_last_pr(storage_path: str = _DEFAULT_PATH) -> int | None:
    """
    Load the number of the last processed pull request.

    Args:
        storage_path: Path to the JSON file used for storage.

    Returns:
        The pull request number, or None if no record exists.
    """
    if not os.path.exists(storage_path):
        return None
    try:
        with open(storage_path, encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("last_pr")
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read storage file %s: %s", storage_path, exc)
        return None
