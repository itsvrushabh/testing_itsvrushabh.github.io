"""Step definitions for responsive design and viewport testing."""
from behave import given, then


@given("I set the browser viewport to {width:d} by {height:d}")
def step_set_viewport(context, width, height):
    if not hasattr(context, "page") or context.page is None:
        context.browser_context = context.browser.new_context(
            viewport={"width": width, "height": height},
            ignore_https_errors=True
        )
        context.page = context.browser_context.new_page()
        from pages.home_page import HomePage
        from pages.terminal_page import TerminalPage
        context.home_page = HomePage(context.page, context.base_url)
        context.terminal_page = TerminalPage(context.page, context.base_url)
    else:
        context.page.set_viewport_size({"width": width, "height": height})


@then("the menubar header should be present")
def step_menubar_present(context):
    assert context.page.locator(".site-header").count() > 0, "Site header element not found in DOM"


@then("the terminal section should be present")
def step_terminal_section_present(context):
    assert context.page.locator("#terminal").count() > 0, "Terminal section not found in DOM"


@then("the hero title should be visible")
def step_hero_title_visible(context):
    assert context.page.locator(".hero-title-name").count() > 0, "Hero title not found in DOM"
