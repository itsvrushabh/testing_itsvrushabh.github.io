"""Terminal Page Object Model for the interactive TUI terminal emulator."""
from pages.base_page import BasePage


class TerminalPage(BasePage):
    SECTION = "#terminal"
    TUI_WINDOW = "#tui-window"
    TUI_OUTPUT = "#tui-output"
    TUI_INPUT = "#tui-input"
    TUI_FORM = "#tui-form"
    
    # Window controls
    BTN_CLOSE = "#tui-btn-close"
    BTN_MIN = "#tui-btn-min"
    BTN_MAX = "#tui-btn-max"

    def scroll_into_view(self) -> None:
        """Scroll terminal into view."""
        self.page.locator(self.SECTION).scroll_into_view_if_needed()

    def click_quick_command(self, cmd_name: str) -> None:
        """Click one of the quick command buttons."""
        selector = f"button.tui-cmd-btn[data-tui-cmd='{cmd_name}']"
        btn = self.page.locator(selector).first
        try:
            btn.scroll_into_view_if_needed(timeout=2000)
            btn.click(timeout=1500)
        except Exception:
            btn.dispatch_event("click")
        self.page.wait_for_timeout(200)

    def type_command(self, command: str) -> None:
        """Type command into terminal input and press Enter."""
        self.page.locator(self.TUI_INPUT).fill(command)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(300)

    def get_output_text(self) -> str:
        """Get accumulated output text from the terminal window."""
        return self.get_text(self.TUI_OUTPUT)

    def clear_output(self) -> None:
        """Click clear quick button or close button to reset terminal."""
        clear_selector = "button.tui-cmd-btn[data-tui-cmd='clear']"
        if self.is_visible(clear_selector):
            btn = self.page.locator(clear_selector).first
            try:
                btn.scroll_into_view_if_needed(timeout=2000)
                btn.click(timeout=1500)
            except Exception:
                btn.dispatch_event("click")
        else:
            self.click(self.BTN_CLOSE)
        self.page.wait_for_timeout(200)
