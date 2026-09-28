"""Step definitions for common navigation and menubar interactions."""
from behave import given, when, then, step
from urllib.parse import urlparse


@given("I visit the website homepage")
@step("I visit the website homepage")
def step_visit_homepage(context):
    if not hasattr(context, "page") or context.page is None:
        context.browser_context = context.browser.new_context(viewport={"width": 1440, "height": 900})
        context.page = context.browser_context.new_page()
        from pages.home_page import HomePage
        from pages.terminal_page import TerminalPage
        context.home_page = HomePage(context.page, context.base_url)
        context.terminal_page = TerminalPage(context.page, context.base_url)

    context.home_page.open()
    context.initial_theme = context.home_page.get_active_theme()


@then('the page title should contain "{keyword}"')
def step_title_contains(context, keyword):
    actual_title = context.page.title()
    assert keyword.lower() in actual_title.lower(), f"Expected '{keyword}' in title, got: '{actual_title}'"


@then("the menubar should be visible")
def step_menubar_visible(context):
    context.home_page.reveal_menubar()
    assert context.home_page.is_visible(context.home_page.HEADER), "Menubar header is not visible"


@then("the home workspace icon should be active")
def step_home_workspace_active(context):
    context.home_page.reveal_menubar()
    home_icon = context.page.locator(context.home_page.NAV_HOME)
    assert "active" in (home_icon.get_attribute("class") or ""), "Home icon does not have 'active' class"


@when('I click on the workspace "{workspace_name}"')
def step_click_workspace(context, workspace_name):
    context.home_page.reveal_menubar()
    locator = context.page.locator(f"nav.menubar-left a[data-ws-name*='{workspace_name}'], nav.menubar-left a[title*='{workspace_name}']").first
    assert locator.is_visible(), f"Workspace '{workspace_name}' was not found in topbar"
    locator.click()
    context.page.wait_for_load_state("domcontentloaded")


@then('the current URL path should be "{expected_path}"')
def step_check_url_path(context, expected_path):
    parsed = urlparse(context.page.url)
    assert parsed.path == expected_path or parsed.path == expected_path.rstrip("/"), \
        f"Expected path '{expected_path}', but got '{parsed.path}' (full URL: {context.page.url})"


@then('the GitHub profile link should point to "{expected_url}"')
def step_check_github_link(context, expected_url):
    context.home_page.reveal_menubar()
    git_link = context.page.locator(context.home_page.GITHUB_LINK).first
    assert git_link.is_visible(), "GitHub link icon not found in menubar"
    href = git_link.get_attribute("href")
    assert href == expected_url, f"Expected GitHub link '{expected_url}', but got '{href}'"


@then("the GitHub profile link should open in a new tab")
def step_check_github_target(context):
    context.home_page.reveal_menubar()
    git_link = context.page.locator(context.home_page.GITHUB_LINK).first
    target = git_link.get_attribute("target")
    assert target == "_blank", f"Expected target='_blank', but got '{target}'"


@when("I click the datetime clock in the menubar")
def step_click_datetime_clock(context):
    context.home_page.reveal_menubar()
    context.home_page.click(context.home_page.DATETIME_BUTTON)
    context.page.wait_for_timeout(300)


@when("I click the datetime clock in the menubar again")
def step_click_datetime_clock_again(context):
    context.home_page.reveal_menubar()
    context.home_page.click(context.home_page.DATETIME_BUTTON)
    context.page.wait_for_timeout(300)


@then("the terminal calendar popover should be displayed")
def step_calendar_popover_displayed(context):
    calendar = context.page.locator(context.home_page.CALENDAR_POPOVER)
    assert calendar.is_visible(), "Terminal calendar popover is not visible"


@then("the terminal calendar popover should be closed")
def step_calendar_popover_closed(context):
    calendar = context.page.locator(context.home_page.CALENDAR_POPOVER)
    is_visible = calendar.is_visible()
    aria_hidden = calendar.get_attribute("aria-hidden")
    assert not is_visible or aria_hidden == "true", "Terminal calendar popover was expected to be closed"


@step("I reload the webpage")
def step_reload_page(context):
    context.page.reload(wait_until="domcontentloaded")
