"""Step definitions for theme toggling and persistence tests."""
from behave import when, then


@then('the active theme attribute on html should be "{expected_theme}"')
def step_check_active_theme(context, expected_theme):
    current_theme = context.home_page.get_active_theme()
    assert current_theme == expected_theme, f"Expected theme '{expected_theme}', but got '{current_theme}'"


@when("I click the theme switcher button")
def step_click_theme_switcher(context):
    context.previous_theme = context.home_page.get_active_theme()
    context.home_page.toggle_theme()


@then("the active theme attribute on html should change from the initial theme")
def step_theme_changed(context):
    current_theme = context.home_page.get_active_theme()
    assert current_theme != context.initial_theme, \
        f"Expected theme to change from '{context.initial_theme}', but remained '{current_theme}'"


@then('the local storage "{key}" should match the active theme')
def step_check_local_storage(context, key):
    ls_theme = context.home_page.get_local_storage_theme()
    current_theme = context.home_page.get_active_theme()
    assert ls_theme == current_theme, \
        f"Local storage key '{key}' ({ls_theme}) does not match active theme ({current_theme})"


@when("I note the current active theme")
def step_note_theme(context):
    context.noted_theme = context.home_page.get_active_theme()


@then("the active theme attribute on html should match the noted theme")
def step_theme_matches_noted(context):
    current_theme = context.home_page.get_active_theme()
    assert current_theme == context.noted_theme, \
        f"Expected theme to persist as '{context.noted_theme}', but got '{current_theme}'"
