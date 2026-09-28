"""Base Page containing reusable web interaction methods using Playwright."""
from typing import Optional
from playwright.sync_api import Page, Locator, Response


class BasePage:
    def __init__(self, page: Page, base_url: str = "https://itsvrushabh.github.io"):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def navigate_to(self, path: str = "/") -> Optional[Response]:
        """Navigate to relative or absolute path."""
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        return self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        """Get document title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Get current URL in the browser."""
        return self.page.url

    def find_element(self, selector: str) -> Locator:
        """Find locator by CSS selector or XPath."""
        return self.page.locator(selector)

    def is_visible(self, selector: str, timeout: float = 5000) -> bool:
        """Check if element is visible within timeout."""
        try:
            return self.page.locator(selector).first.is_visible(timeout=timeout)
        except Exception:
            return False

    def click(self, selector: str, timeout: float = 5000, force: bool = False) -> None:
        """Click element by selector with automatic fallback for animated elements."""
        locator = self.page.locator(selector).first
        try:
            locator.scroll_into_view_if_needed(timeout=timeout)
            locator.click(timeout=timeout, force=force)
        except Exception:
            locator.dispatch_event("click")

    def get_text(self, selector: str) -> str:
        """Get text content of first matching element."""
        return self.page.locator(selector).first.inner_text().strip()

    def get_attribute(self, selector: str, attr_name: str) -> Optional[str]:
        """Get attribute value of first matching element."""
        return self.page.locator(selector).first.get_attribute(attr_name)

    def take_screenshot(self, filepath: str) -> bytes:
        """Capture screenshot to disk."""
        return self.page.screenshot(path=filepath, full_page=True)

    def evaluate_js(self, expression: str):
        """Execute JavaScript expression in the page context."""
        return self.page.evaluate(expression)
