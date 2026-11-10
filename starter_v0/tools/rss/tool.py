from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err


def _local_name(tag: str) -> str:
    return tag.split("}")[-1]


def _child_text(entry: ET.Element, name: str) -> str:
    for child in entry:
        if _local_name(child.tag) == name and (child.text or "").strip():
            return child.text.strip()
    return ""


def _link_of(entry: ET.Element) -> str:
    for child in entry:
        if _local_name(child.tag) != "link":
            continue
        href = (child.get("href") or "").strip()
        if href:
            return href
        text = (child.text or "").strip()
        if text:
            return text
    return ""


def _entry_item(entry: ET.Element, source: str) -> dict[str, Any]:
    summary = (
        _child_text(entry, "description")
        or _child_text(entry, "summary")
        or _child_text(entry, "content")
    )
    date = (
        _child_text(entry, "pubDate")
        or _child_text(entry, "published")
        or _child_text(entry, "updated")
    )
    return {
        "title": _child_text(entry, "title"),
        "url": _link_of(entry),
        "source": source,
        "summary": summary,
        "date": date,
    }


def get_rss_items(feed_url: str = "", limit: int = 5) -> dict[str, Any]:
    """Read one RSS/Atom feed and return items in the shared digest format."""
    try:
        feed_url = str(feed_url or "").strip()
        if not feed_url.lower().startswith(("http://", "https://")):
            raise ValueError("feed_url must be a valid http(s) URL")
        response = requests.get(feed_url, timeout=TIMEOUT)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        source = domain(feed_url)
        entries = [el for el in root.iter() if _local_name(el.tag) in ("item", "entry")]
        items = [_entry_item(entry, source) for entry in entries]
        return {"tool": "get_rss_items", "feed_url": feed_url, "items": items[: int(limit or 5)]}
    except Exception as exc:
        return err("get_rss_items", exc)
