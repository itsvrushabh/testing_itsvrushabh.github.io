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
        self.click(selector, force=True)
        self.page.wait_for_timeout(300)

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
        if self.is_visible("button.tui-cmd-btn[data-tui-cmd='clear']"):
            self.click("button.tui-cmd-btn[data-tui-cmd='clear']", force=True)
        else:
            self.click(self.BTN_CLOSE, force=True)
        self.page.wait_for_timeout(200)
