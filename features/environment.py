"""Behave environment hooks for Playwright browser setup, teardown, and failure screenshots."""
import os
import re
from playwright.sync_api import sync_playwright
from pages.home_page import HomePage
from pages.terminal_page import TerminalPage


def sanitize_filename(name: str) -> str:
    """Sanitize string for safe filesystem filename."""
    return re.sub(r"[^\w\-_]", "_", name)


def before_all(context):
    """Set up test environment, directories, and browser."""
    # Ensure artifacts directories exist
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # Read config from behave userdata or use defaults
    context.base_url = context.config.userdata.get("base_url", "https://itsvrushabh.github.io").rstrip("/")
    context.headless = context.config.userdata.get("headless", "true").lower() == "true"
    browser_name = context.config.userdata.get("browser", "chromium").lower()
    slow_mo = int(context.config.userdata.get("slow_mo", 0))

    # Initialize Playwright
    context.playwright = sync_playwright().start()
    browser_type = getattr(context.playwright, browser_name, context.playwright.chromium)
    
    launch_kwargs = {"headless": context.headless, "slow_mo": slow_mo}
    exec_path = context.config.userdata.get("executable_path")
    if not exec_path:
        for candidate in ["/usr/bin/chromium", "/usr/bin/google-chrome-stable", "/usr/bin/firefox"]:
            if os.path.exists(candidate) and ("chromium" in candidate or "chrome" in candidate if browser_name == "chromium" else browser_name in candidate):
                exec_path = candidate
                break
    if exec_path:
        launch_kwargs["executable_path"] = exec_path

    try:
        context.browser = browser_type.launch(**launch_kwargs)
    except Exception:
        launch_kwargs.pop("executable_path", None)
        context.browser = browser_type.launch(**launch_kwargs)


def before_scenario(context, scenario):
    """Create fresh browser context and page objects for each scenario."""
    if "api" in scenario.effective_tags:
        context.page = None
        return

    context.browser_context = context.browser.new_context(
        viewport={"width": 1440, "height": 900},
        ignore_https_errors=True,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 BDD-Test-Runner"
    )
    context.page = context.browser_context.new_page()
    context.home_page = HomePage(context.page, context.base_url)
    context.terminal_page = TerminalPage(context.page, context.base_url)


def after_scenario(context, scenario):
    """Take screenshot on failure and clean up browser context."""
    if hasattr(context, "page") and context.page is not None:
        if scenario.status == "failed":
            filename = f"screenshots/FAIL_{sanitize_filename(scenario.name)}.png"
            try:
                context.page.screenshot(path=filename, full_page=True)
                print(f"\n[BDD HOOK] Screenshot saved to {filename}")
            except Exception as e:
                print(f"\n[BDD HOOK] Failed to capture screenshot: {e}")

        try:
            context.page.close()
            context.browser_context.close()
        except Exception:
            pass


def after_all(context):
    """Shut down browser and Playwright."""
    if hasattr(context, "browser") and context.browser:
        context.browser.close()
    if hasattr(context, "playwright") and context.playwright:
        context.playwright.stop()
