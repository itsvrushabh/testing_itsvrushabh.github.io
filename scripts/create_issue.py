#!/usr/bin/env python3
"""Script to report automated test failures as an issue on GitHub."""
import os
import sys
import subprocess
import glob


TARGET_REPO = "itsvrushabh/itsvrushabh.github.io"
ISSUE_TITLE = "🚨 [Automated Test] Health Check Failure on itsvrushabh.github.io"


def get_token() -> str:
    """Return available GitHub token from environment."""
    return os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN") or ""


def get_failure_summary(log_file: str = "test-output.log") -> str:
    """Extract failure snippet from the test log."""
    if not os.path.exists(log_file):
        return "Log file not found."
    
    with open(log_file, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    # Capture the last 60 lines containing error summaries
    recent_lines = lines[-60:] if len(lines) > 60 else lines
    return "".join(recent_lines)


def get_failure_screenshots() -> list[str]:
    """List screenshots captured during test failure."""
    return glob.glob("screenshots/FAIL_*.png")


def create_or_update_issue():
    token = get_token()
    if not token:
        print("[WARNING] Neither GH_PAT nor GITHUB_TOKEN is set. Skipping GitHub Issue creation.")
        return

    os.environ["GH_TOKEN"] = token
    env_name = os.environ.get("GITHUB_EVENT_NAME", "manual")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "testing_itsvrushabh.github.io")
    run_url = f"{server_url}/{repo}/actions/runs/{run_id}" if run_id else "Local / Manual run"

    failure_log = get_failure_summary()
    screenshots = get_failure_screenshots()
    screenshots_text = "\n".join([f"- `{os.path.basename(s)}`" for s in screenshots]) if screenshots else "None"

    body = f"""### 🚨 Automated Website Test Failure Detected

A test failure occurred while executing the automated BDD test suite against **https://itsvrushabh.github.io**.

#### 📋 Execution Details
- **Target URL:** https://itsvrushabh.github.io
- **Triggered By:** `{env_name}`
- **Workflow Run:** [{run_id or 'Link'}]({run_url})
- **Failed Screenshots:**
{screenshots_text}

#### 🪵 Test Failure Output (Last 60 lines)
```text
{failure_log}
```

---
*Generated automatically by BDD Test Automation Suite.*
"""

    print(f"Checking for existing open issues on {TARGET_REPO}...")
    try:
        check_cmd = [
            "gh", "issue", "list",
            "--repo", TARGET_REPO,
            "--state", "open",
            "--search", "Automated Test Health Check Failure",
            "--json", "number",
            "-q", ".[0].number"
        ]
        result = subprocess.run(check_cmd, capture_output=True, text=True)
        existing_issue_number = result.stdout.strip()

        if existing_issue_number and existing_issue_number.isdigit():
            print(f"Found existing open issue #{existing_issue_number}. Adding comment...")
            comment_cmd = [
                "gh", "issue", "comment", existing_issue_number,
                "--repo", TARGET_REPO,
                "--body", f"### ⚠️ Recurring Failure Encountered\n\nRun: {run_url}\n\n```text\n{failure_log[-1500:]}\n```"
            ]
            subprocess.run(comment_cmd, check=True)
            print(f"Successfully commented on issue #{existing_issue_number}.")
        else:
            print(f"Creating new issue on {TARGET_REPO}...")
            create_cmd = [
                "gh", "issue", "create",
                "--repo", TARGET_REPO,
                "--title", ISSUE_TITLE,
                "--body", body
            ]
            res = subprocess.run(create_cmd, capture_output=True, text=True, check=True)
            print(f"Successfully created issue: {res.stdout.strip()}")

    except Exception as e:
        print(f"[ERROR] Failed to create or update issue on {TARGET_REPO}: {e}")
        # Do not fail the overall step to avoid masking root test failure
        sys.exit(0)


if __name__ == "__main__":
    create_or_update_issue()
