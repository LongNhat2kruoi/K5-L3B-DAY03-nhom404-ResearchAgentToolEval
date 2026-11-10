from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import streamlit as st

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from chat import run_model_tool_loop  # noqa: E402
from env_loader import load_lab_env  # noqa: E402
from execution_trace import make_event, new_request_id  # noqa: E402
from providers import make_provider  # noqa: E402
from tools import load_tool_declarations, to_openai_tools  # noqa: E402


load_lab_env(ROOT)
st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="wide")


def render_value(value: Any) -> None:
    if isinstance(value, (dict, list)):
        st.json(value, expanded=False)
    else:
        st.code(str(value))


def render_trace(events: list[dict[str, Any]], descriptions: dict[str, str]) -> None:
    if not events:
        st.info("No execution event yet.")
        return
    st.caption(f"Request ID: {events[0].get('request_id', 'unknown')}")
    for index, event in enumerate(events, start=1):
        event_type = event.get("event_type", "unknown")
        data = event.get("data") or {}
        status = data.get("status", "info")
        icon = {"completed": "✅", "failed": "❌", "running": "🔄", "pending": "⏳"}.get(status, "ℹ️")
        with st.expander(f"{icon} {index}. {event_type}", expanded=event_type == "tool_failed"):
            st.caption(f"{event.get('timestamp', 'unknown')} · status={status}")
            tool_name = data.get("tool_name")
            if tool_name:
                st.markdown(f"**Tool:** `{tool_name}`")
                if descriptions.get(tool_name):
                    st.caption(f"Purpose: {descriptions[tool_name]}")
            if "duration_ms" in data:
                st.caption(f"Duration: {data['duration_ms']} ms")
            if "input" in data:
                st.markdown("**Input parameters**")
                render_value(data["input"])
            if "output" in data:
                st.markdown("**Tool output**")
                render_value(data["output"])
            if event_type == "tool_failed":
                st.error("Tool execution failed.")


def trace_box(events: list[dict[str, Any]], descriptions: dict[str, str]) -> None:
    """The only place where execution status is shown in the UI."""
    with st.container(border=True):
        st.markdown("### Execution Logs / Tool Calling Trace")
        render_trace(events, descriptions)


def main() -> None:
    st.title("Research Agent")
    st.write("Ask a research question and inspect the actual tool execution trace in the box below.")

    with st.sidebar:
        st.header("Configuration")
        provider_name = st.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini", "ollama"])
        version = st.text_input("Artifact version", "v3")
        max_rounds = st.number_input("Maximum tool rounds", min_value=1, max_value=8, value=4)
        if st.button("Clear conversation"):
            st.session_state.messages = []
            st.session_state.trace_events = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "trace_events" not in st.session_state:
        st.session_state.trace_events = []

    declarations = load_tool_declarations(ROOT / "artifacts" / "tools.yaml")
    descriptions = {item["name"]: item.get("description", "") for item in declarations}

    st.subheader("Conversation")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Persistent, dedicated trace box. It is not a chat message and does not use
    # a thinking spinner; the backend events are rendered here as they arrive.
    trace_box(st.session_state.trace_events, descriptions)

    prompt = st.chat_input("Enter a research question...")
    if not prompt:
        return

    request_id = new_request_id()
    st.session_state.trace_events = [make_event(request_id, "query_received", {"query": prompt, "status": "completed"})]
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        system_prompt = (ROOT / "artifacts" / "system_prompt.md").read_text(encoding="utf-8")
        provider = make_provider(provider_name)
        tools = to_openai_tools(declarations)
        trace_placeholder = st.empty()

        def on_event(event: dict[str, Any]) -> None:
            st.session_state.trace_events.append(event)
            with trace_placeholder.container():
                trace_box(st.session_state.trace_events, descriptions)

        result = run_model_tool_loop(
            provider=provider,
            messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages],
            tools=tools,
            model=None,
            max_tool_rounds=int(max_rounds),
            request_id=request_id,
            event_sink=on_event,
        )
        st.session_state.messages.append({"role": "assistant", "content": result.get("assistant_text", "")})
        st.rerun()
    except Exception as exc:
        st.session_state.trace_events.append(make_event(
            request_id,
            "execution_error",
            {"status": "failed", "error": f"{type(exc).__name__}: {exc}"},
        ))
        st.error(f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
