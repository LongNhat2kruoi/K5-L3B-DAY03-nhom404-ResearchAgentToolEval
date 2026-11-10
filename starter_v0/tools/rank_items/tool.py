from __future__ import annotations

from typing import Any


def rank_research_items(
    items: list[dict[str, Any]] | None = None,
    sort_by: str = "score",
    descending: bool = True,
) -> dict[str, Any]:
    try:
        if not isinstance(items, list):
            raise ValueError("items must be a list")
        if sort_by not in {"score", "title", "source"}:
            raise ValueError("sort_by must be one of: score, title, source")

        def key(item: dict[str, Any]) -> Any:
            value = item.get(sort_by, 0 if sort_by == "score" else "")
            return float(value or 0) if sort_by == "score" else str(value or "").casefold()

        ranked = sorted(items, key=key, reverse=bool(descending))
        return {"tool": "rank_research_items", "sort_by": sort_by, "descending": bool(descending), "items": ranked, "item_count": len(ranked)}
    except Exception as exc:
        return {"tool": "rank_research_items", "error": type(exc).__name__, "message": str(exc)}
