"""OpenAI client for summarizing pull requests into a structured changelog."""

import json
import os

from openai import OpenAI

from src.ai.prompts import build_changelog_prompt
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OpenAIClient:
    """Uses the OpenAI API to generate a structured changelog from pull request data."""

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """
        Initialize the OpenAI client.

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

        prompt = build_changelog_prompt(pull_requests, version)
        logger.debug("Sending prompt to OpenAI model '%s'...", self.model)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3,
        )

        content = response.choices[0].message.content
        result = json.loads(content)
        logger.info("Changelog summary generated successfully.")
        return result
