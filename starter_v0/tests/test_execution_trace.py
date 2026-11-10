from __future__ import annotations

from chat import run_model_tool_loop
from providers.base import ModelResponse, ToolCall


class FakeProvider:
    def complete(self, messages, tools=None, *, model=None, temperature=0.0, tool_choice=None):
        return ModelResponse(tool_calls=[ToolCall("clarify", {"question": "Which account?"})])


def test_tool_loop_emits_correlated_trace_events() -> None:
    events = []
    result = run_model_tool_loop(
        provider=FakeProvider(),
        messages=[{"role": "user", "content": "recent posts"}],
        tools=[],
        model=None,
        max_tool_rounds=1,
        request_id="req_test",
        event_sink=events.append,
    )

    assert result["status"] == "waiting_for_user"
    assert events
    assert all(event["request_id"] == "req_test" for event in events)
    assert {event["event_type"] for event in events} >= {"agent_started", "tool_selected", "tool_started", "tool_completed"}


def test_trace_sanitizes_credential_fields() -> None:
    events = []

    class CredentialProvider:
        def complete(self, messages, tools=None, *, model=None, temperature=0.0, tool_choice=None):
            return ModelResponse(text="done")

    run_model_tool_loop(
        provider=CredentialProvider(),
        messages=[{"role": "user", "content": "hello"}],
        tools=[],
        model=None,
        max_tool_rounds=1,
        request_id="req_secret",
        event_sink=events.append,
    )
    from execution_trace import make_event

    event = make_event("req_secret", "test", {"api_key": "do-not-log", "safe": "ok"})
    assert event["data"]["api_key"] == "[REDACTED]"
    assert event["data"]["safe"] == "ok"
