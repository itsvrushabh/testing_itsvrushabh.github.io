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
    current_repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_url = f"{server_url}/{current_repo}/actions/runs/{run_id}" if run_id and current_repo else "Local / Manual run"

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

    # First attempt TARGET_REPO (itsvrushabh/itsvrushabh.github.io).
    # If cross-repo token is not configured, fall back to current_repo.
    target_repos = [TARGET_REPO]
    if current_repo and current_repo != TARGET_REPO:
        target_repos.append(current_repo)

    for repo in target_repos:
        print(f"Attempting to record test failure issue on {repo}...")
        try:
            check_cmd = [
                "gh", "issue", "list",
                "--repo", repo,
                "--state", "open",
                "--search", "Automated Test Health Check Failure",
                "--json", "number",
                "-q", ".[0].number"
            ]
            result = subprocess.run(check_cmd, capture_output=True, text=True, check=True)
            existing_issue_number = result.stdout.strip()

            if existing_issue_number and existing_issue_number.isdigit():
                print(f"Found existing open issue #{existing_issue_number} on {repo}. Adding comment...")
                comment_cmd = [
                    "gh", "issue", "comment", existing_issue_number,
                    "--repo", repo,
                    "--body", f"### ⚠️ Recurring Failure Encountered\n\nRun: {run_url}\n\n```text\n{failure_log[-1500:]}\n```"
                ]
                subprocess.run(comment_cmd, check=True)
                print(f"Successfully commented on issue #{existing_issue_number} on {repo}.")
                return
            else:
                print(f"Creating new issue on {repo}...")
                create_cmd = [
                    "gh", "issue", "create",
                    "--repo", repo,
                    "--title", ISSUE_TITLE,
                    "--body", body
                ]
                res = subprocess.run(create_cmd, capture_output=True, text=True, check=True)
                print(f"Successfully created issue on {repo}: {res.stdout.strip()}")
                return

        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip() if e.stderr else str(e)
            print(f"[NOTICE] Could not manage issue on {repo}: {err_msg}")
            if repo == TARGET_REPO and len(target_repos) > 1:
                print(f"[INFO] Cross-repo access to {TARGET_REPO} requires secret 'GH_PAT'. Falling back to local repo {current_repo}...")
                continue
            break


if __name__ == "__main__":
    create_or_update_issue()
