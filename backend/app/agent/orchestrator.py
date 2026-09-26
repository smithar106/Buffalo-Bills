"""Agent orchestrator.

USER QUESTION → PLAN/SELECT TOOLS → READ-ONLY TOOLS → STRUCTURED EVIDENCE
→ LLM REASONING → GROUNDING/VALIDATION → ANSWER + SOURCES
"""

from __future__ import annotations

import json
import time
from typing import Any

from app.providers.llm import LLMClient, LLMError
from app.providers.sports import get_sports_provider
from app.services.observability import record_agent_run, record_mlflow

from .grounding import build_fallback_answer, validate_answer
from .prompts import RETRY_INSTRUCTION, build_system_prompt, build_user_prompt
from .tools import TOOL_SCHEMAS, ToolRunner

MAX_TOOL_ITERATIONS = 5


class AgentResult(dict):
    """Convenience dict wrapper for a structured agent result."""


def _tool_call_messages(completion: dict[str, Any]) -> tuple[list[dict], list[dict]]:
    """Convert an LLM completion's tool_calls into assistant + tool messages."""
    llm = LLMClient()
    calls = llm.tool_calls(completion)
    assistant_msg = {
        "role": "assistant",
        "content": None,
        "tool_calls": calls,
    }
    tool_msgs = []
    for call in calls:
        args = llm.parse_tool_args(call)
        tool_msgs.append((call["id"], call["function"]["name"], args))
    return [assistant_msg], tool_msgs


def _build_sources(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = []
    seen = set()
    for e in evidence:
        key = (e["tool"], e["source"])
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            {
                "label": e["source"],
                "tool": e["tool"],
                "retrieved_at": e["retrieved_at"],
                "evidence": json.dumps(e.get("payload", {}), default=str)[:2000],
            }
        )
    return sources


def run(question: str, mode: str | None = None, context: str | None = None) -> AgentResult:
    started = time.monotonic()
    llm = LLMClient()
    runner = ToolRunner()

    tool_calls_log: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []

    result: AgentResult = AgentResult(
        answer="",
        mode=mode or "bills_mafia",
        sources=[],
        demo=get_sports_provider().label == "mock",
        fallback=False,
        validation={"result": "ok", "unsupported": []},
        tool_calls=[],
        llm_latency_ms=None,
        total_latency_ms=None,
    )

    if not llm.configured:
        result["answer"] = "I couldn't verify that from the available Bills data."
        result["fallback"] = True
        result["validation"] = {"result": "no_llm", "unsupported": []}
        result["total_latency_ms"] = int((time.monotonic() - started) * 1000)
        record_agent_run(
            question, result["mode"], tool_calls_log, evidence,
            None, result["total_latency_ms"], "no_llm", True,
        )
        return result

    # Determine the current season to give the agent accurate context.
    current_season = None
    try:
        current_season = get_sports_provider().get_next_game().season
    except Exception:
        current_season = None

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": build_system_prompt(mode, current_season)},
        {"role": "user", "content": build_user_prompt(question, context)},
    ]

    answer = ""
    last_completion: dict[str, Any] | None = None

    try:
        for _ in range(MAX_TOOL_ITERATIONS):
            completion = llm.chat(messages, tools=TOOL_SCHEMAS)
            last_completion = completion
            result["llm_latency_ms"] = completion.get("_latency_ms")

            if not llm.tool_calls(completion):
                answer = llm.message_text(completion)
                break

            assistant_msgs, requested = _tool_call_messages(completion)
            messages.extend(assistant_msgs)

            for call_id, name, args in requested:
                ev = runner.execute(name, args)
                evidence.append(ev)
                tool_calls_log.append(
                    {"tool": name, "arguments": args, "latency_ms": ev["latency_ms"]}
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call_id,
                        "name": name,
                        "content": json.dumps(ev["payload"], default=str),
                    }
                )

        # If we exhausted iterations on tool calls, force a final grounded answer.
        if not answer:
            completion = llm.chat(messages, tools=None)
            last_completion = completion
            answer = llm.message_text(completion)

    except LLMError:
        result["answer"] = build_fallback_answer(evidence)
        result["fallback"] = True
        result["validation"] = {"result": "llm_error", "unsupported": []}
        result["sources"] = _build_sources(evidence)
        result["tool_calls"] = tool_calls_log
        result["total_latency_ms"] = int((time.monotonic() - started) * 1000)
        record_agent_run(
            question, result["mode"], tool_calls_log, evidence,
            result["llm_latency_ms"], result["total_latency_ms"], "llm_error", True,
        )
        return result

    # Grounding validation.
    unsupported = validate_answer(answer, evidence)
    if unsupported and evidence:
        # Retry once with stronger grounding instructions.
        retry_messages = messages + [
            {
                "role": "user",
                "content": RETRY_INSTRUCTION + json.dumps([e["payload"] for e in evidence], default=str),
            }
        ]
        try:
            completion = llm.chat(retry_messages, tools=None)
            result["llm_latency_ms"] = completion.get("_latency_ms")
            retried = llm.message_text(completion)
            unsupported = validate_answer(retried, evidence)
            if not unsupported:
                answer = retried
                result["validation"] = {"result": "retried", "unsupported": []}
            else:
                answer = build_fallback_answer(evidence)
                result["fallback"] = True
                result["validation"] = {"result": "fallback", "unsupported": unsupported}
        except LLMError:
            answer = build_fallback_answer(evidence)
            result["fallback"] = True
            result["validation"] = {"result": "fallback", "unsupported": unsupported}
    elif unsupported and not evidence:
        # No tools were called but the answer contains numbers → fallback.
        answer = "I couldn't verify that from the available Bills data."
        result["fallback"] = True
        result["validation"] = {"result": "fallback", "unsupported": unsupported}

    result["answer"] = answer
    result["sources"] = _build_sources(evidence)
    result["tool_calls"] = tool_calls_log
    result["total_latency_ms"] = int((time.monotonic() - started) * 1000)

    record_agent_run(
        question, result["mode"], tool_calls_log, evidence,
        result["llm_latency_ms"], result["total_latency_ms"],
        result["validation"]["result"], result["fallback"],
    )
    record_mlflow(
        question,
        result["mode"],
        {
            "llm_latency_ms": result["llm_latency_ms"] or 0,
            "total_latency_ms": result["total_latency_ms"],
            "tool_calls": len(tool_calls_log),
            "fallback": int(result["fallback"]),
            "sources": len(result["sources"]),
        },
    )
    return result
