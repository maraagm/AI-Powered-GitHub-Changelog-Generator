"""OpenAI integration for summarizing pull requests into a structured changelog."""

import json
import os

from openai import OpenAI


class ChangelogSummarizer:
    """Uses the OpenAI API to generate a structured changelog from pull request data."""

    # Categories used to group pull requests in the changelog
    CATEGORIES = ["Features", "Bug Fixes", "Improvements", "Documentation", "Other"]

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """
        Initialize the summarizer.

        Args:
            api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
            model: OpenAI model to use for summarization.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
            )

        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def _build_prompt(self, pull_requests: list[dict], version: str) -> str:
        """
        Build the prompt that is sent to the OpenAI API.

        Args:
            pull_requests: Enriched list of pull request dictionaries.
            version: Version string for the changelog entry (e.g. "v1.2.0").

        Returns:
            Formatted prompt string.
        """
        pr_descriptions = []
        for pr in pull_requests:
            files_summary = (
                ", ".join(pr["changed_files"][:10])
                if pr["changed_files"]
                else "no files listed"
            )
            if len(pr["changed_files"]) > 10:
                files_summary += f" and {len(pr['changed_files']) - 10} more"

            pr_descriptions.append(
                f"PR #{pr['number']} by @{pr['user']} (merged {pr['merged_at'][:10]})\n"
                f"Title: {pr['title']}\n"
                f"Description: {pr['body'][:500] if pr['body'] else 'No description'}\n"
                f"Changed files: {files_summary}\n"
                f"Labels: {', '.join(pr['labels']) if pr['labels'] else 'none'}"
            )

        prs_text = "\n\n".join(pr_descriptions)
        categories_list = ", ".join(self.CATEGORIES)

        return (
            f"You are a technical writer generating a structured software changelog.\n\n"
            f"Version: {version}\n\n"
            f"The following pull requests were merged:\n\n{prs_text}\n\n"
            f"Generate a structured changelog entry for version {version}. "
            f"Group the changes into the following categories where applicable: "
            f"{categories_list}. "
            f"Return ONLY a JSON object with this structure:\n"
            f'{{"version": "{version}", "summary": "brief overall summary", '
            f'"categories": {{"Features": ["item1", ...], "Bug Fixes": [...], '
            f'"Improvements": [...], "Documentation": [...], "Other": [...]}}}}\n\n'
            f"Only include categories that have at least one item. "
            f"Keep each item concise (one sentence). "
            f"Focus on user-facing impact rather than implementation details."
        )

    def summarize(self, pull_requests: list[dict], version: str) -> dict:
        """
        Summarize pull requests into a structured changelog using OpenAI.

        Args:
            pull_requests: Enriched list of pull request dictionaries.
            version: Version string for the changelog entry.

        Returns:
            Dictionary with keys: version, summary, and categories.
        """
        if not pull_requests:
            return {
                "version": version,
                "summary": "No pull requests to summarize.",
                "categories": {},
            }

        prompt = self._build_prompt(pull_requests, version)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3,
        )

        content = response.choices[0].message.content
        result = json.loads(content)
        return result
