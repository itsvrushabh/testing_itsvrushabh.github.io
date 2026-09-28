"""Step definitions for keyboard shortcut navigation."""
from behave import when, then


@when('I press keyboard key "{key}"')
def step_press_key(context, key):
    # If key is backquote, playwright key is Backquote or `
    key_name = "Backquote" if key == "`" else key
    context.page.keyboard.press(key_name)
    context.page.wait_for_timeout(300)


@when('I press key combination "{key_combo}"')
def step_press_key_combination(context, key_combo):
    context.page.keyboard.press(key_combo)
    context.page.wait_for_timeout(300)


@then("the shortcuts modal dialog should be displayed")
def step_shortcuts_modal_displayed(context):
    modal = context.page.locator("#shortcuts-modal")
    modal_class = modal.get_attribute("class") or ""
    assert "visible" in modal_class, f"Shortcuts modal does not have 'visible' class: {modal_class}"


@then("the shortcuts modal dialog should be closed")
def step_shortcuts_modal_closed(context):
    modal = context.page.locator("#shortcuts-modal")
    modal_class = modal.get_attribute("class") or ""
    assert "visible" not in modal_class, f"Shortcuts modal unexpectedly has 'visible' class: {modal_class}"


@then("the command palette dialog should be displayed")
def step_palette_modal_displayed(context):
    modal = context.page.locator("#command-palette-modal")
    modal_class = modal.get_attribute("class") or ""
    assert "visible" in modal_class, f"Command palette does not have 'visible' class: {modal_class}"


@then("the command palette dialog should be closed")
def step_palette_modal_closed(context):
    modal = context.page.locator("#command-palette-modal")
    modal_class = modal.get_attribute("class") or ""
    assert "visible" not in modal_class, f"Command palette unexpectedly has 'visible' class: {modal_class}"


@then("the interactive terminal input should be focused")
def step_terminal_input_focused(context):
    focused_id = context.page.evaluate("document.activeElement?.id || ''")
    assert focused_id == "tui-input", f"Expected activeElement id 'tui-input', got '{focused_id}'"
