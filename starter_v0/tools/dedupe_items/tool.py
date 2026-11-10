from __future__ import annotations

from typing import Any


def deduplicate_research_items(items: list[dict[str, Any]] | None = None, key: str = "url") -> dict[str, Any]:
    try:
        if not isinstance(items, list):
            raise ValueError("items must be a list")
        if key not in {"url", "title", "source"}:
            raise ValueError("key must be one of: url, title, source")
        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for item in items:
            value = str(item.get(key, "")).strip().casefold()
            if not value or value in seen:
                continue
            seen.add(value)
            unique.append(item)
        return {"tool": "deduplicate_research_items", "key": key, "items": unique, "removed_count": len(items) - len(unique)}
    except Exception as exc:
        return {"tool": "deduplicate_research_items", "error": type(exc).__name__, "message": str(exc)}
