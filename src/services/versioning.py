"""Version detection and semantic versioning utilities."""

import re


def normalize_version(version: str) -> str:
    """
    Ensure a version string starts with 'v'.

    Args:
        version: Raw version string such as '1.2.3' or 'v1.2.3'.

    Returns:
        Version string prefixed with 'v', e.g. 'v1.2.3'.
    """
    version = version.strip()
    if not version.startswith("v"):
        version = f"v{version}"
    return version


def validate_version(version: str) -> bool:
    """
    Validate that a version string follows semantic versioning (vMAJOR.MINOR.PATCH).

    Args:
        version: Version string to validate (e.g. 'v1.2.3').

    Returns:
        True if the version is valid, False otherwise.
    """
    pattern = r"^v?\d+\.\d+\.\d+$"
    return bool(re.match(pattern, version))


def detect_bump_type(pull_requests: list[dict]) -> str:
    """
    Detect the appropriate version bump type based on PR labels.

    Examines labels on each pull request and returns 'major', 'minor', or 'patch'
    according to the highest-impact label found.

    Args:
        pull_requests: List of pull request dictionaries with a 'labels' key.

    Returns:
        One of 'major', 'minor', or 'patch'.
    """
    all_labels: set[str] = set()
    for pr in pull_requests:
        all_labels.update(label.lower() for label in pr.get("labels", []))

    if any(label in all_labels for label in ("breaking", "major", "breaking-change")):
        return "major"
    if any(label in all_labels for label in ("feature", "minor", "enhancement")):
        return "minor"
    return "patch"
