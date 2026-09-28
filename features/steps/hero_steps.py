"""Step definitions for Hero section and snippet switcher."""
from behave import when, then


@then('the hero title should be "{expected_title}"')
def step_check_hero_title(context, expected_title):
    title = context.home_page.get_hero_title()
    assert title.strip() == expected_title.strip(), f"Expected hero title '{expected_title}', got '{title}'"


@then('the hero tagline should contain "{keyword}"')
def step_check_hero_tagline(context, keyword):
    tagline = context.home_page.get_hero_tagline()
    assert keyword.lower() in tagline.lower(), f"Expected tagline to contain '{keyword}', got '{tagline}'"


@then('the hero lead description should mention "{keyword}"')
def step_check_hero_lead(context, keyword):
    lead = context.home_page.get_hero_lead()
    assert keyword.lower() in lead.lower(), f"Expected lead text to mention '{keyword}', got '{lead}'"


@when('I click the snippet tab "{snippet_mode}"')
def step_click_snippet_tab(context, snippet_mode):
    context.home_page.select_snippet_tab(snippet_mode)


@then('the snippet command label should contain "{expected_snippet_text}"')
def step_check_snippet_label(context, expected_snippet_text):
    label = context.home_page.get_text(context.home_page.SNIPPET_LABEL)
    assert expected_snippet_text in label, \
        f"Expected snippet label to contain '{expected_snippet_text}', got '{label}'"


@then('the "{button_text}" button should link to "{expected_link}"')
def step_check_button_link(context, button_text, expected_link):
    btn = context.page.locator(f"a:has-text('{button_text}')").first
    assert btn.is_visible(), f"Button with text '{button_text}' not visible"
    href = btn.get_attribute("href")
    assert href == expected_link, f"Expected button to link to '{expected_link}', but got '{href}'"
