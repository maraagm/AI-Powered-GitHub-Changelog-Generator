"""HTML renderer for generating beautiful changelog HTML pages using Jinja2."""

import os
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.utils.logger import get_logger

logger = get_logger(__name__)

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"


class HTMLRenderer:
    """Renders changelog data as a styled HTML page using a Jinja2 template."""

    def __init__(
        self,
        template_name: str = "changelog.html",
        output_path: str = "output/changelog.html",
    ):
        """
        Initialize the HTML renderer.

        Args:
            template_name: Name of the Jinja2 template file inside the templates/ directory.
            output_path: Path where the rendered HTML file will be written.
        """
        self.output_path = output_path
        self.env = Environment(
            loader=FileSystemLoader(str(_TEMPLATES_DIR)),
            autoescape=select_autoescape(["html"]),
        )
        self.template = self.env.get_template(template_name)

    def render(self, changelog_data: dict) -> str:
        """
        Render the changelog data as an HTML string.

        Args:
            changelog_data: Dictionary with keys version, summary, and categories.

        Returns:
            Rendered HTML string.
        """
        context = {
            "version": changelog_data.get("version", "Unreleased"),
            "summary": changelog_data.get("summary", ""),
            "categories": changelog_data.get("categories", {}),
            "generated_at": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        }
        return self.template.render(**context)

    def write(self, changelog_data: dict) -> None:
        """
        Render the changelog and write it to the output HTML file.

        Args:
            changelog_data: Dictionary with keys version, summary, and categories.
        """
        html_content = self.render(changelog_data)
        os.makedirs(os.path.dirname(self.output_path) or ".", exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as fh:
            fh.write(html_content)

        logger.info("HTML changelog written to %s", self.output_path)
        print(f"HTML changelog written to {self.output_path}")
