"""Step definitions for testing interactive TUI terminal emulator."""
import time
from behave import given, when, then


@given("I navigate to the interactive terminal section")
def step_navigate_terminal_section(context):
    context.terminal_page.scroll_into_view()
    context.page.wait_for_timeout(300)


@then("the terminal window should be visible")
def step_terminal_window_visible(context):
    assert context.terminal_page.is_visible(context.terminal_page.TUI_WINDOW), "Terminal window is not visible"


@then('the terminal prompt should show "{expected_prompt}"')
def step_terminal_prompt(context, expected_prompt):
    prompt_text = context.page.locator(".tui-prompt").first.inner_text().strip()
    assert expected_prompt in prompt_text, f"Expected prompt '{expected_prompt}', got '{prompt_text}'"


@when('I click the quick command button "{command}"')
def step_click_quick_cmd(context, command):
    context.terminal_page.click_quick_command(command)


@then('the terminal output should contain "{expected_content}"')
def step_terminal_output_contains(context, expected_content):
    timeout = 5.0
    start = time.time()
    output = ""
    while time.time() - start < timeout:
        output = context.terminal_page.get_output_text()
        if expected_content.lower() in output.lower():
            return
        context.page.wait_for_timeout(200)
    assert expected_content.lower() in output.lower(), \
        f"Expected terminal output to contain '{expected_content}', but got:\n{output}"


@when('I type "{command}" into the terminal prompt and submit')
def step_type_terminal_command(context, command):
    context.terminal_page.type_command(command)


@then('the terminal output should match either "{content1}" or "{content2}"')
def step_terminal_output_contains_either(context, content1, content2):
    timeout = 5.0
    start = time.time()
    output = ""
    while time.time() - start < timeout:
        output = context.terminal_page.get_output_text()
        if content1.lower() in output.lower() or content2.lower() in output.lower():
            return
        context.page.wait_for_timeout(200)
    matched = content1.lower() in output.lower() or content2.lower() in output.lower()
    assert matched, f"Expected output to contain '{content1}' or '{content2}', but got:\n{output}"


@then("the terminal output should not be empty")
def step_terminal_output_not_empty(context):
    timeout = 5.0
    start = time.time()
    output = ""
    while time.time() - start < timeout:
        output = context.terminal_page.get_output_text()
        if len(output.strip()) > 0:
            return
        context.page.wait_for_timeout(200)
    assert len(output.strip()) > 0, "Terminal output is empty"


@then("the terminal output should be cleared")
def step_terminal_output_cleared(context):
    timeout = 5.0
    start = time.time()
    output = ""
    while time.time() - start < timeout:
        output = context.terminal_page.get_output_text()
        if output == "" or len(output.strip()) == 0:
            return
        context.page.wait_for_timeout(200)
    assert output == "" or len(output.strip()) == 0, f"Expected terminal output to be cleared, but got: {output}"
