"""Changelog generation service: builds and writes CHANGELOG.md."""

import os
from datetime import datetime, timezone

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ChangelogService:
    """Generates and manages the CHANGELOG.md file."""

    def __init__(self, output_path: str = "output/CHANGELOG.md"):
        """
        Initialize the changelog service.

        Args:
            output_path: Path to the CHANGELOG.md file.
        """
        self.output_path = output_path

    def _format_entry(self, changelog_data: dict) -> str:
        """
        Format a single changelog entry as a Markdown string.

        Args:
            changelog_data: Dictionary with keys version, summary, and categories.

        Returns:
            Markdown-formatted changelog entry.
        """
        version = changelog_data.get("version", "Unreleased")
        summary = changelog_data.get("summary", "")
        categories = changelog_data.get("categories", {})
        date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

        lines = [f"## [{version}] - {date_str}", ""]

        if summary:
            lines += [summary, ""]

        for category, items in categories.items():
            if items:
                lines.append(f"### {category}")
                lines += [f"- {item}" for item in items]
                lines.append("")

        return "\n".join(lines)

    def _build_header(self) -> str:
        """Return the standard CHANGELOG.md header."""
        return (
            "# Changelog\n\n"
            "All notable changes to this project will be documented in this file.\n\n"
            "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).\n\n"
        )

    def write(self, changelog_data: dict) -> None:
        """
        Write a new CHANGELOG.md file with the provided entry.

        If the file already exists the new entry is prepended after the header,
        preserving all previous entries.

        Args:
            changelog_data: Dictionary returned by OpenAIClient.summarize().
        """
        new_entry = self._format_entry(changelog_data)

        os.makedirs(os.path.dirname(self.output_path) or ".", exist_ok=True)

        if os.path.exists(self.output_path):
            with open(self.output_path, encoding="utf-8") as fh:
                existing_content = fh.read()

            # Find where the first version entry starts so we can insert before it
            header = self._build_header()
            if existing_content.startswith(header):
                rest = existing_content[len(header):]
            else:
                # Preserve whatever header is already there
                header_end = existing_content.find("\n## ")
                if header_end == -1:
                    header = existing_content
                    rest = ""
                else:
                    header = existing_content[: header_end + 1]
                    rest = existing_content[header_end + 1:]

            updated_content = header + new_entry + "\n" + rest
        else:
            updated_content = self._build_header() + new_entry

        with open(self.output_path, "w", encoding="utf-8") as fh:
            fh.write(updated_content)

        logger.info("Changelog written to %s", self.output_path)
        print(f"Changelog written to {self.output_path}")

    def preview(self, changelog_data: dict) -> str:
        """
        Return the formatted changelog entry without writing to disk.

        Args:
            changelog_data: Dictionary returned by OpenAIClient.summarize().

        Returns:
            Markdown-formatted changelog entry string.
        """
        return self._format_entry(changelog_data)
