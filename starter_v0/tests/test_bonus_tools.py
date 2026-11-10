from __future__ import annotations

from tools import TOOL_FUNCTIONS


def test_rank_items_orders_scores_descending() -> None:
    result = TOOL_FUNCTIONS["rank_items"](
        [{"title": "low", "score": 0.1}, {"title": "high", "score": 0.9}],
        "score",
        True,
    )
    assert [item["title"] for item in result["items"]] == ["high", "low"]


def test_rank_items_rejects_invalid_sort_field() -> None:
    result = TOOL_FUNCTIONS["rank_items"]([], "date", True)
    assert result["error"] == "ValueError"


def test_rank_items_rejects_non_list_input() -> None:
    result = TOOL_FUNCTIONS["rank_items"]("invalid", "score", True)
    assert result["error"] == "ValueError"


def test_dedupe_items_removes_duplicate_urls() -> None:
    result = TOOL_FUNCTIONS["dedupe_items"](
        [{"url": "https://a.test"}, {"url": "https://a.test"}, {"url": "https://b.test"}],
        "url",
    )
    assert len(result["items"]) == 2
    assert result["removed_count"] == 1


def test_dedupe_items_rejects_invalid_key() -> None:
    result = TOOL_FUNCTIONS["dedupe_items"]([], "date")
    assert result["error"] == "ValueError"


def test_dedupe_items_rejects_non_list_input() -> None:
    result = TOOL_FUNCTIONS["dedupe_items"]("invalid", "url")
    assert result["error"] == "ValueError"
