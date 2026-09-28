#!/usr/bin/env python3
"""Script to automatically resolve and close open test failure issues on GitHub when tests pass."""
import os
import sys
import subprocess
from datetime import datetime, timezone


TARGET_REPO = "itsvrushabh/itsvrushabh.github.io"
ISSUE_SEARCH_QUERY = "Automated Test Health Check Failure"


def get_token() -> str:
    """Return available GitHub token from environment."""
    return os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN") or ""


def resolve_open_issues():
    token = get_token()
    if not token:
        print("[INFO] Neither GH_PAT nor GITHUB_TOKEN is set. Skipping issue resolution check.")
        return

    os.environ["GH_TOKEN"] = token
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    current_repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_url = f"{server_url}/{current_repo}/actions/runs/{run_id}" if run_id and current_repo else "Local / Manual run"
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    target_repos = [TARGET_REPO]
    if current_repo and current_repo != TARGET_REPO:
        target_repos.append(current_repo)

    for repo in target_repos:
        print(f"Checking for open test failure issues on {repo}...")
        try:
            check_cmd = [
                "gh", "issue", "list",
                "--repo", repo,
                "--state", "open",
                "--search", ISSUE_SEARCH_QUERY,
                "--json", "number,title",
                "-q", ".[].number"
            ]
            result = subprocess.run(check_cmd, capture_output=True, text=True, check=True)
            issue_numbers = result.stdout.strip().split()

            if not issue_numbers:
                print(f"No open automated test failure issues found on {repo}.")
                continue

            for issue_num in issue_numbers:
                print(f"Resolving and closing issue #{issue_num} on {repo}...")
                resolution_comment = f"""### ✅ Automated Test Suite Passed — Issue Resolved

The automated BDD test suite executed against **https://itsvrushabh.github.io** and all tests passed successfully with 0 errors.

- **Status:** All Scenarios Passed
- **Resolution Run:** [{run_id or 'Details'}]({run_url})
- **Resolved At:** `{now_utc}`

*Closing issue automatically.*
"""
                close_cmd = [
                    "gh", "issue", "close", issue_num,
                    "--repo", repo,
                    "--comment", resolution_comment,
                    "--reason", "completed"
                ]
                subprocess.run(close_cmd, check=True)
                print(f"Successfully closed issue #{issue_num} on {repo}.")

        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip() if e.stderr else str(e)
            print(f"[NOTICE] Could not query or close issues on {repo}: {err_msg}")
            continue


if __name__ == "__main__":
    resolve_open_issues()
