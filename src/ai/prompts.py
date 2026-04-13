"""Prompt templates for generating AI-powered changelogs."""

# Categories used to group pull requests in the changelog
CATEGORIES = ["Features", "Bug Fixes", "Improvements", "Documentation", "Other"]


def build_changelog_prompt(pull_requests: list[dict], version: str) -> str:
    """
    Build the prompt sent to the OpenAI API to generate a structured changelog.

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
    categories_list = ", ".join(CATEGORIES)

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
