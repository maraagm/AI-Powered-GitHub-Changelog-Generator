"""
AI-Powered GitHub Changelog Generator
======================================
Entry point for the changelog generation pipeline.

Usage:
    python main.py --version v1.2.0 [--repo owner/repo] [--limit 50] [--output CHANGELOG.md]

Environment variables:
    GITHUB_TOKEN        GitHub personal access token (required)
    GITHUB_REPOSITORY   Repository in 'owner/repo' format (required if --repo not provided)
    OPENAI_API_KEY      OpenAI API key (required)
"""

import argparse
import sys

from src.ai.summarizer import ChangelogSummarizer
from src.github.client import GitHubClient
from src.services.changelog import ChangelogService
from src.utils.helpers import normalize_version, validate_version


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate an AI-powered changelog from merged GitHub pull requests."
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Version string for this changelog entry, e.g. '1.2.0' or 'v1.2.0'.",
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Repository in 'owner/repo' format. Overrides GITHUB_REPOSITORY env var.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of merged PRs to include (default: 50).",
    )
    parser.add_argument(
        "--output",
        default="CHANGELOG.md",
        help="Output path for the changelog file (default: CHANGELOG.md).",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use for summarization (default: gpt-4o-mini).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the changelog entry to stdout instead of writing to a file.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the changelog generation pipeline."""
    args = parse_args()

    # Validate and normalise the version string
    version = normalize_version(args.version)
    if not validate_version(version):
        print(
            f"Error: '{args.version}' is not a valid semantic version (expected MAJOR.MINOR.PATCH).",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Generating changelog for version {version}...")

    # 1. Fetch merged pull requests from GitHub
    print("Fetching merged pull requests from GitHub...")
    github_client = GitHubClient(repo=args.repo)
    pull_requests = github_client.get_merged_pull_requests(limit=args.limit)

    if not pull_requests:
        print("No merged pull requests found. Exiting.")
        sys.exit(0)

    print(f"Found {len(pull_requests)} merged pull request(s). Fetching file changes...")
    pull_requests = github_client.enrich_pull_requests(pull_requests)

    # 2. Summarise pull requests with OpenAI
    print("Summarising changes with OpenAI...")
    summarizer = ChangelogSummarizer(model=args.model)
    changelog_data = summarizer.summarize(pull_requests, version)

    # 3. Generate the changelog
    service = ChangelogService(output_path=args.output)

    if args.dry_run:
        print("\n--- Changelog Preview ---\n")
        print(service.preview(changelog_data))
    else:
        service.write(changelog_data)
        print("Done!")


if __name__ == "__main__":
    main()
