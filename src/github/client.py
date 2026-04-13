"""GitHub API client for fetching merged pull requests."""

import os
import requests

from src.utils.logger import get_logger

logger = get_logger(__name__)


class GitHubClient:
    """Client for interacting with the GitHub REST API."""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str = None, repo: str = None):
        """
        Initialize the GitHub client.

        Args:
            token: GitHub personal access token. Falls back to GITHUB_TOKEN env var.
            repo: Repository in 'owner/repo' format. Falls back to GITHUB_REPOSITORY env var.
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo = repo or os.getenv("GITHUB_REPOSITORY")

        if not self.token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable.")
        if not self.repo:
            raise ValueError(
                "Repository is required. Set GITHUB_REPOSITORY environment variable "
                "in 'owner/repo' format."
            )

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    def get_merged_pull_requests(self, limit: int = 50) -> list[dict]:
        """
        Fetch recently merged pull requests from the repository.

        Args:
            limit: Maximum number of pull requests to retrieve.

        Returns:
            List of pull request data dictionaries.
        """
        url = f"{self.BASE_URL}/repos/{self.repo}/pulls"
        params = {
            "state": "closed",
            "sort": "updated",
            "direction": "desc",
            "per_page": min(limit, 100),
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()

        # Filter to only merged pull requests
        all_prs = response.json()
        merged_prs = [pr for pr in all_prs if pr.get("merged_at") is not None]
        logger.debug("Fetched %d merged PR(s) from GitHub.", len(merged_prs))

        return merged_prs[:limit]

    def get_pull_request_files(self, pr_number: int) -> list[dict]:
        """
        Fetch the list of files changed in a pull request.

        Args:
            pr_number: The pull request number.

        Returns:
            List of file change data dictionaries.
        """
        url = f"{self.BASE_URL}/repos/{self.repo}/pulls/{pr_number}/files"
        response = self.session.get(url, params={"per_page": 100})
        response.raise_for_status()
        return response.json()

