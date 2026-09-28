"""Step definitions for critical assets and performance budget checks."""
import requests
from behave import when, then


@when('I request the static asset "{asset_path}"')
def step_request_asset(context, asset_path):
    base_url = getattr(context, "base_url", "https://itsvrushabh.github.io").rstrip("/")
    url = f"{base_url}{asset_path}"
    context.asset_response = requests.get(url, timeout=10)


@then("the asset status code should be {status_code:d}")
def step_assert_asset_status(context, status_code):
    assert context.asset_response.status_code == status_code, \
        f"Expected status {status_code}, got {context.asset_response.status_code} for {context.asset_response.url}"


@then('the asset content-type should be "{expected_type}"')
def step_assert_asset_content_type(context, expected_type):
    content_type = context.asset_response.headers.get("content-type", "")
    assert expected_type in content_type, \
        f"Expected '{expected_type}' in content-type, but got '{content_type}'"


@then("the asset size should be less than {max_size_kb:d} kilobytes")
def step_assert_asset_size(context, max_size_kb):
    content_len = len(context.asset_response.content)
    size_kb = content_len / 1024
    assert size_kb <= max_size_kb, \
        f"Asset size {size_kb:.2f} KB exceeds maximum budget of {max_size_kb} KB"


@then("the DOMContentLoaded duration should be under {max_ms:d} milliseconds")
def step_assert_dom_timing(context, max_ms):
    timing = context.page.evaluate("""() => {
        const perf = performance.getEntriesByType('navigation')[0];
        return perf ? (perf.domContentLoadedEventEnd - perf.startTime) : 0;
    }""")
    assert timing <= max_ms, f"DOMContentLoaded took {timing:.1f}ms, exceeding budget of {max_ms}ms"
