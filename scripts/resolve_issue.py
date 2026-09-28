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
    repo = os.environ.get("GITHUB_REPOSITORY", "testing_itsvrushabh.github.io")
    run_url = f"{server_url}/{repo}/actions/runs/{run_id}" if run_id else "Local / Manual run"
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    print(f"Checking for open automated test failure issues on {TARGET_REPO}...")
    try:
        check_cmd = [
            "gh", "issue", "list",
            "--repo", TARGET_REPO,
            "--state", "open",
            "--search", ISSUE_SEARCH_QUERY,
            "--json", "number,title",
            "-q", ".[].number"
        ]
        result = subprocess.run(check_cmd, capture_output=True, text=True)
        issue_numbers = result.stdout.strip().split()

        if not issue_numbers:
            print("No open automated test failure issues found. System is healthy.")
            return

        for issue_num in issue_numbers:
            print(f"Resolving and closing issue #{issue_num} on {TARGET_REPO}...")
            resolution_comment = f"""### ✅ Automated Test Suite Passed — Issue Resolved

The automated BDD test suite executed against **https://itsvrushabh.github.io** and all tests passed successfully with 0 errors.

- **Status:** All Scenarios Passed
- **Resolution Run:** [{run_id or 'Details'}]({run_url})
- **Resolved At:** `{now_utc}`

*Closing issue automatically.*
"""
            close_cmd = [
                "gh", "issue", "close", issue_num,
                "--repo", TARGET_REPO,
                "--comment", resolution_comment,
                "--reason", "completed"
            ]
            subprocess.run(close_cmd, check=True)
            print(f"Successfully closed issue #{issue_num}.")

    except Exception as e:
        print(f"[ERROR] Failed during issue resolution on {TARGET_REPO}: {e}")
        sys.exit(0)


if __name__ == "__main__":
    resolve_open_issues()
