"""Step definitions for crawling and detecting broken links."""
import re
import requests
from urllib.parse import urljoin
from behave import when, then


@when("I crawl all internal links from the homepage")
def step_crawl_internal_links(context):
    base_url = getattr(context, "base_url", "https://itsvrushabh.github.io").rstrip("/")
    resp = requests.get(base_url, timeout=10)
    assert resp.status_code == 200, f"Failed to fetch homepage: status {resp.status_code}"

    # Extract all hrefs starting with / or ./
    raw_links = set(re.findall(r'href=[\"\'](/[^\"\'#]*|\./[^\"\'#]*)[\"\']', resp.text))
    context.checked_links = {}

    for link in sorted(raw_links):
        # Exclude static image/css/feed files from full HTML route crawling
        if any(link.endswith(ext) for ext in [".css", ".js", ".svg", ".webp", ".png", ".ico", ".xml", ".opml"]):
            continue
        full_url = urljoin(base_url, link)
        try:
            r = requests.get(full_url, timeout=10)
            context.checked_links[link] = r.status_code
        except Exception as e:
            context.checked_links[link] = f"ERROR: {e}"


@then("none of the crawled internal links should return 404 or server errors")
def step_assert_no_broken_links(context):
    broken = {link: status for link, status in context.checked_links.items() if status != 200}
    assert not broken, f"Discovered broken internal links: {broken}"
