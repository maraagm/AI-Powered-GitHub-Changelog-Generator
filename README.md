# AI-Powered GitHub Changelog Generator

AI-powered tool that analyzes merged pull requests and automatically generates structured changelogs. Integrates with GitHub workflows to summarize code changes into clear, human-readable release notes, reducing manual documentation effort and improving project visibility.

---

## Features

- **GitHub Integration** – Fetches merged pull requests including title, description, and changed files.
- **AI Summarization** – Uses OpenAI to group changes into categories (Features, Bug Fixes, Improvements, Documentation, Other).
- **Changelog Generation** – Produces a `CHANGELOG.md` file in [Keep a Changelog](https://keepachangelog.com) format.
- **GitHub Actions Ready** – Includes a workflow that triggers on release publication or manual dispatch.

---

## Project Structure

```
.
├── main.py                        # Entry point
├── requirements.txt               # Python dependencies
├── .env.example                   # Example environment variables
├── .github/
│   └── workflows/
│       └── changelog.yml          # GitHub Actions workflow
└── src/
    ├── github/
    │   └── client.py              # GitHub API client
    ├── ai/
    │   └── summarizer.py          # OpenAI summarization
    ├── services/
    │   └── changelog.py           # Changelog file generation
    └── utils/
        └── helpers.py             # Shared utilities
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/maraagm/AI-Powered-GitHub-Changelog-Generator.git
cd AI-Powered-GitHub-Changelog-Generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

| Variable             | Description                                      |
|----------------------|--------------------------------------------------|
| `GITHUB_TOKEN`       | GitHub personal access token (repo read access)  |
| `GITHUB_REPOSITORY`  | Target repository in `owner/repo` format         |
| `OPENAI_API_KEY`     | Your OpenAI API key                              |

---

## Usage

### Command line

```bash
# Generate and write CHANGELOG.md
python main.py --version 1.2.0

# Preview without writing to disk
python main.py --version 1.2.0 --dry-run

# Target a specific repository and limit PR count
python main.py --version 1.2.0 --repo owner/repo --limit 30

# Use a different OpenAI model
python main.py --version 1.2.0 --model gpt-4o
```

### GitHub Actions

Add the following secrets to your repository:

- `OPENAI_API_KEY` – your OpenAI API key (`GITHUB_TOKEN` is provided automatically).

The workflow runs automatically when a GitHub Release is published. It can also be triggered manually from the **Actions** tab using **Run workflow**.

---

## Output

The generated `CHANGELOG.md` follows the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [v1.2.0] - 2025-04-10

Brief overall summary of this release.

### Features
- Added support for multiple repositories.

### Bug Fixes
- Fixed authentication error when token is missing.

### Improvements
- Reduced API calls by caching PR file lists.
```

---

## Requirements

- Python 3.12+
- GitHub personal access token with `repo` (read) scope
- OpenAI API key
