"""Unit tests for the team tool `cite_source` (offline, pure local)."""
from __future__ import annotations

import pytest

from tools import TOOL_FUNCTIONS

cite = TOOL_FUNCTIONS["cite_source"]


def test_cite_official_source_is_tier1_with_author_date_and_domain_link() -> None:
    result = cite(
        title="Introducing GPT-5",
        url="https://www.openai.com/blog/gpt-5",
        source_type="official",
        author="OpenAI",
        date="2026-06-01",
    )

    assert result["citation"] == "OpenAI (2026-06-01). Introducing GPT-5. [openai.com](https://www.openai.com/blog/gpt-5)"
    assert result["tier"] == 1
    assert result["label"] == "primary source"


def test_cite_arxiv_includes_arxiv_id_and_preprint_label() -> None:
    result = cite(
        title="Attention Is All You Need",
        url="https://arxiv.org/abs/1706.03762",
        source_type="arxiv",
        arxiv_id="1706.03762",
    )

    assert "arXiv:1706.03762." in result["citation"]
    assert result["tier"] == 1
    assert "not peer reviewed" in result["label"]


def test_cite_social_source_is_tier3_and_flagged_unverified() -> None:
    result = cite(title="Big claim", url="https://x.com/someone/status/1", source_type="social", author="someone")

    assert result["tier"] == 3
    assert result["label"] == "early signal / unverified"


def test_cite_unknown_source_type_defaults_to_unverified_tier3() -> None:
    result = cite(title="Blog post", url="https://example.com/post")

    assert result["source_type"] == "other"
    assert result["tier"] == 3


@pytest.mark.parametrize("title", ["", "   ", None])
def test_cite_empty_title_returns_error_dict_instead_of_raising(title) -> None:
    result = cite(title=title, url="https://example.com")

    assert result["error"] == "ValueError"
    assert "title" in result["message"]
    assert "citation" not in result


@pytest.mark.parametrize("url", ["", "example.com/no-scheme", "ftp://example.com/file", 123])
def test_cite_invalid_url_returns_error_dict(url) -> None:
    result = cite(title="Some title", url=url)

    assert result["error"] == "ValueError"
    assert "url" in result["message"]


def test_cite_source_type_outside_enum_returns_error_dict() -> None:
    result = cite(title="Some title", url="https://example.com", source_type="blog")

    assert result["error"] == "ValueError"
    assert "source_type" in result["message"]


def test_cite_source_type_is_case_insensitive_and_trimmed() -> None:
    result = cite(title="Some title", url="https://example.com", source_type="  News ")

    assert result["source_type"] == "news"
    assert result["tier"] == 2
