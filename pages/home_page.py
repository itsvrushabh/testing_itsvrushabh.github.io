"""Home Page Object Model for itsvrushabh.github.io."""
from typing import Optional, List
from pages.base_page import BasePage


class HomePage(BasePage):
    # Header selectors
    HEADER = ".site-header"
    NAV_HOME = "nav.menubar-left a.mb-home"
    NAV_PROJECTS = "nav.menubar-left a[href='/projects/']"
    NAV_BLOG = "nav.menubar-left a[href='/blog/']"
    NAV_ABOUT = "nav.menubar-left a[href='/about/']"
    NAV_CONTACT = "nav.menubar-left a[href='/contact/']"
    NAV_RESUME = "nav.menubar-left a[href='/resume/']"
    
    DATETIME_BUTTON = "#menubar-datetime"
    CALENDAR_POPOVER = "#menubar-calendar-popover"
    THEME_BUTTON = "#theme-toggle-btn"
    MUSIC_BUTTON = "#header-music-toggle"
    GITHUB_LINK = ".menubar-right a[href*='github.com']"
    PALETTE_BUTTON = "#open-palette-btn"
    SHORTCUTS_BUTTON = "[data-open-shortcuts]"

    # Hero selectors
    HERO_TITLE = ".hero-title-name"
    HERO_TAGLINE = ".hero-tagline"
    HERO_LEAD = ".hero-lead"
    SNIPPET_TAB_CARGO = "button.snippet-tab-btn[data-snippet-mode='cargo']"
    SNIPPET_TAB_CURL = "button.snippet-tab-btn[data-snippet-mode='curl']"
    SNIPPET_TAB_CLI = "button.snippet-tab-btn[data-snippet-mode='cli']"
    SNIPPET_LABEL = "#hero-snippet-label"
    COPY_INSTALL_BTN = "#copy-install-btn"
    CTA_TERMINAL = "a.btn-omarchy-primary"
    CTA_PROJECTS = "a.btn-omarchy-secondary"

    def open(self) -> None:
        """Open the homepage."""
        self.navigate_to("/")

    def reveal_menubar(self) -> None:
        """Scroll slightly to trigger header reveal animation if hidden."""
        self.page.evaluate("window.scrollTo(0, 350)")
        self.page.wait_for_timeout(300)

    def get_hero_title(self) -> str:
        self.page.locator(self.HERO_TITLE).scroll_into_view_if_needed()
        return self.get_text(self.HERO_TITLE)

    def get_hero_tagline(self) -> str:
        self.page.locator(self.HERO_TAGLINE).scroll_into_view_if_needed()
        return self.get_text(self.HERO_TAGLINE)

    def get_hero_lead(self) -> str:
        self.page.locator(self.HERO_LEAD).scroll_into_view_if_needed()
        return self.get_text(self.HERO_LEAD)

    def get_active_theme(self) -> str:
        """Get dataset theme attribute on <html> element."""
        return self.evaluate_js("document.documentElement.dataset.theme || ''")

    def toggle_theme(self) -> str:
        """Click theme button and return new theme."""
        self.reveal_menubar()
        prev_theme = self.get_active_theme()
        self.click(self.THEME_BUTTON)
        self.page.wait_for_timeout(300)
        return self.get_active_theme()

    def get_local_storage_theme(self) -> str:
        """Get theme saved in localStorage."""
        return self.evaluate_js("localStorage.getItem('omarchy-site-theme') || ''")

    def toggle_calendar(self) -> bool:
        """Click clock button to toggle terminal calendar popover."""
        self.reveal_menubar()
        self.click(self.DATETIME_BUTTON)
        self.page.wait_for_timeout(200)
        return self.is_visible(self.CALENDAR_POPOVER)

    def is_calendar_open(self) -> bool:
        """Check if calendar popover is active/visible."""
        return self.evaluate_js(
            "document.getElementById('menubar-calendar-popover')?.classList.contains('active') || "
            "document.getElementById('menubar-calendar-popover')?.getAttribute('aria-hidden') === 'false'"
        )

    def select_snippet_tab(self, mode: str) -> str:
        """Switch snippet tabs (cargo, curl, cli) and return snippet label text."""
        tab_selector = f"button.snippet-tab-btn[data-snippet-mode='{mode}']"
        self.page.locator(tab_selector).dispatch_event("click")
        self.page.wait_for_timeout(200)
        return self.get_text(self.SNIPPET_LABEL)

    def get_nav_items(self) -> List[str]:
        """Get list of workspace numbers/links available in topbar."""
        items = self.page.locator("nav.menubar-left a.mb-item").all()
        return [item.get_attribute("title") or item.inner_text().strip() for item in items]
