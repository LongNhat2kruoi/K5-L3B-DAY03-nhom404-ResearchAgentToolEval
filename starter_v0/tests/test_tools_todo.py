"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

wiki_tool = TOOL_FUNCTIONS["wiki"]


def test_wiki_builds_request_url_and_maps_summary(fake_http) -> None:
    calls = fake_http(FakeResponse({
        "type": "standard",
        "title": "Large language model",
        "description": "Type of machine learning model",
        "extract": "A large language model (LLM) is ...",
        "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Large_language_model"}},
    }))

    result = wiki_tool(title="Large language model", lang="en")

    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == "https://en.wikipedia.org/api/rest_v1/page/summary/Large_language_model"
    assert "User-Agent" in calls[0]["headers"]
    assert result["found"] is True
    assert result["is_disambiguation"] is False
    assert result["summary"].startswith("A large language model")
    assert result["url"] == "https://en.wikipedia.org/wiki/Large_language_model"


def test_wiki_rejects_empty_title_without_calling_network(fake_http) -> None:
    calls = fake_http(FakeResponse({}))
    assert wiki_tool(title="   ")["error"] == "ValueError"
    assert wiki_tool(title=None)["error"] == "ValueError"
    assert calls == []


def test_wiki_rejects_lang_that_would_change_hostname(fake_http) -> None:
    calls = fake_http(FakeResponse({}))
    result = wiki_tool(title="AI", lang="evil.com/x")
    assert result["error"] == "ValueError"
    assert calls == []


def test_wiki_404_means_not_found_not_error(fake_http) -> None:
    fake_http(FakeResponse(status_code=404))
    result = wiki_tool(title="Khong ton tai xyz", lang="vi")
    assert result["found"] is False
    assert "error" not in result


def test_wiki_http_error_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=503))
    assert wiki_tool(title="AI")["error"] == "HTTPError"


RSS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>VNExpress</title>
  <item><title>Tin 1</title><link>https://vnexpress.net/tin-1</link>
    <description>Mo ta 1</description><pubDate>Mon, 09 Nov 2026 10:00:00 +0700</pubDate></item>
  <item><title>Tin 2</title><link>https://vnexpress.net/tin-2</link>
    <description>Mo ta 2</description><pubDate>Mon, 09 Nov 2026 09:00:00 +0700</pubDate></item>
  <item><title>Tin 3</title><link>https://vnexpress.net/tin-3</link>
    <description>Mo ta 3</description><pubDate>Mon, 09 Nov 2026 08:00:00 +0700</pubDate></item>
</channel></rss>"""

rss_tool = TOOL_FUNCTIONS["rss"]


def test_rss_maps_items_and_respects_limit(fake_http) -> None:
    fake_http(FakeResponse(content=RSS_XML.encode("utf-8")))
    result = rss_tool(feed_url="https://vnexpress.net/rss/tin-moi-nhat.rss", limit=2)

    assert result["tool"] == "get_rss_items"
    assert len(result["items"]) == 2
    assert result["items"][0]["title"] == "Tin 1"
    assert result["items"][0]["source"] == "vnexpress.net"


def test_rss_rejects_url_without_scheme_and_makes_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse(content=b""))
    result = rss_tool(feed_url="khong-phai-url")

    assert result["error"] == "ValueError"
    assert calls == []


def test_rss_http_error_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=429))
    result = rss_tool(feed_url="https://example.com/feed.rss")

    assert result["error"] == "HTTPError"
    assert result["tool"] == "get_rss_items"


def test_rss_malformed_xml_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(content=b"this is not xml"))
    result = rss_tool(feed_url="https://example.com/feed.rss")

    assert result["error"] == "ParseError"
    assert result["tool"] == "get_rss_items"
