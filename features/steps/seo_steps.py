"""Step definitions for SEO metadata, Open Graph tags, and HTTP health checks."""
import requests
from behave import when, then


@when('I perform an HTTP GET request to "{endpoint}"')
def step_http_get_request(context, endpoint):
    base_url = getattr(context, "base_url", "https://itsvrushabh.github.io").rstrip("/")
    url = f"{base_url}{endpoint}"
    context.http_response = requests.get(url, timeout=10)


@then("the response status code should be {status_code:d}")
def step_check_status_code(context, status_code):
    assert context.http_response.status_code == status_code, \
        f"Expected status {status_code}, got {context.http_response.status_code} for {context.http_response.url}"


@then('the response content-type should be "{content_type}"')
def step_check_content_type(context, content_type):
    actual_ct = context.http_response.headers.get("content-type", "")
    assert content_type in actual_ct, \
        f"Expected content-type to contain '{content_type}', got '{actual_ct}'"


@then('the meta tag "{name}" should have content "{expected_content}"')
def step_check_meta_content(context, name, expected_content):
    meta = context.page.locator(f"meta[name='{name}']").first
    assert meta.count() > 0, f"Meta tag with name='{name}' not found"
    content = meta.get_attribute("content") or ""
    assert content.strip() == expected_content.strip(), \
        f"Expected meta {name} content '{expected_content}', got '{content}'"


@then('the meta tag "{name}" should not be empty')
def step_meta_not_empty(context, name):
    meta = context.page.locator(f"meta[name='{name}']").first
    assert meta.count() > 0, f"Meta tag with name='{name}' not found"
    content = meta.get_attribute("content") or ""
    assert len(content.strip()) > 0, f"Meta tag {name} content is empty"


@then('the open graph tag "{prop}" should contain "{expected_content}"')
def step_check_og_content(context, prop, expected_content):
    og = context.page.locator(f"meta[property='{prop}']").first
    assert og.count() > 0, f"OG meta tag with property='{prop}' not found"
    content = og.get_attribute("content") or ""
    assert expected_content.lower() in content.lower(), \
        f"Expected og tag {prop} to contain '{expected_content}', got '{content}'"


@then('the link tag "{rel}" should point to "{expected_href}"')
def step_check_link_tag(context, rel, expected_href):
    link = context.page.locator(f"link[rel='{rel}']").first
    assert link.count() > 0, f"Link tag with rel='{rel}' not found"
    href = link.get_attribute("href") or ""
    assert href == expected_href, f"Expected link {rel} to point to '{expected_href}', got '{href}'"
