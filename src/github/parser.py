"""Processes and enriches raw GitHub pull request data."""

import requests

from src.github.client import GitHubClient
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PRParser:
    """Parses and enriches raw pull request data fetched from the GitHub API."""

    def __init__(self, client: GitHubClient):
        """
        Initialize the parser.

        Args:
            client: An authenticated GitHubClient instance.
        """
        self.client = client

    def enrich(self, pull_requests: list[dict]) -> list[dict]:
        """
        Enrich pull request data with changed file information.

        Args:
            pull_requests: List of raw pull request dictionaries from the GitHub API.

        Returns:
            List of enriched pull request dictionaries including changed files.
        """
        enriched = []
        for pr in pull_requests:
            pr_number = pr["number"]
            try:
                files = self.client.get_pull_request_files(pr_number)
                changed_files = [f["filename"] for f in files]
            except requests.HTTPError as exc:
                logger.warning(
                    "Could not fetch files for PR #%s: %s", pr_number, exc
                )
                changed_files = []

            enriched.append(
                {
                    "number": pr_number,
                    "title": pr.get("title", ""),
                    "body": pr.get("body") or "",
                    "merged_at": pr.get("merged_at", ""),
                    "user": pr.get("user", {}).get("login", "unknown"),
                    "labels": [label["name"] for label in pr.get("labels", [])],
                    "changed_files": changed_files,
                }
            )

        return enriched
