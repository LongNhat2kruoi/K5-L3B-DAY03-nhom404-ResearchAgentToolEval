from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from tools._shared import domain, err

SOURCE_TYPES = ("official", "paper", "arxiv", "news", "social", "other")

_TIERS = {
    "official": (1, "primary source"),
    "paper": (1, "primary source"),
    "arxiv": (1, "preprint - claims are from the authors, not peer reviewed"),
    "news": (2, "secondary reporting - link to primary evidence if available"),
    "social": (3, "early signal / unverified"),
    "other": (3, "early signal / unverified"),
}


def format_citation(
    title: str = "",
    url: str = "",
    source_type: str = "other",
    author: str = "",
    date: str = "",
    arxiv_id: str = "",
) -> dict[str, Any]:
    try:
        title = str(title or "").strip()
        url = str(url or "").strip()
        author = str(author or "").strip()
        date = str(date or "").strip()
        arxiv_id = str(arxiv_id or "").strip()
        source_type = str(source_type or "other").strip().lower()

        if not title:
            raise ValueError("title is required")
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("url must be a full http(s) URL")
        if source_type not in SOURCE_TYPES:
            raise ValueError(f"source_type must be one of {', '.join(SOURCE_TYPES)}")

        tier, label = _TIERS[source_type]
        head = " ".join(part for part in (author, f"({date})" if date else "") if part)
        parts = [f"{head}." if head else "", f"{title}."]
        if source_type == "arxiv" and arxiv_id:
            parts.append(f"arXiv:{arxiv_id}.")
        parts.append(f"[{domain(url)}]({url})")
        citation = " ".join(part for part in parts if part)
        return {
            "tool": "format_citation",
            "citation": citation,
            "tier": tier,
            "label": label,
            "source_type": source_type,
        }
    except Exception as exc:
        return err("format_citation", exc)
