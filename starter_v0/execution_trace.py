from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any, Callable


TraceSink = Callable[[dict[str, Any]], None]
_SECRET_KEY = re.compile(r"(api[_-]?key|token|password|secret|authorization|credential)", re.I)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def new_request_id() -> str:
    return f"req_{uuid.uuid4().hex}"


def sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]" if _SECRET_KEY.search(str(key)) else sanitize(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [sanitize(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def make_event(request_id: str, event_type: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "event_id": f"evt_{uuid.uuid4().hex}",
        "event_type": event_type,
        "timestamp": now_iso(),
        "data": sanitize(data),
    }
