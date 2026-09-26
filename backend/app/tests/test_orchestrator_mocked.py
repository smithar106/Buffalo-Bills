"""Deterministic orchestrator tests using a scripted (fake) LLM."""

import json

import app.agent.orchestrator as orch
from app.agent import run


class ScriptedLLM:
    def __init__(self, tool_name, tool_args, answer):
        self.configured = True
        self.tool_name = tool_name
        self.tool_args = tool_args
        self.answer = answer
        self.issued_tool = False

    def chat(self, messages, tools=None, **kwargs):
        if tools and not self.issued_tool:
            self.issued_tool = True
            return {
                "_latency_ms": 1,
                "choices": [
                    {
                        "message": {
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": "c1",
                                    "type": "function",
                                    "function": {
                                        "name": self.tool_name,
                                        "arguments": json.dumps(self.tool_args),
                                    },
                                }
                            ],
                        }
                    }
                ],
            }
        return {
            "_latency_ms": 1,
            "choices": [{"message": {"content": self.answer}}],
        }

    def tool_calls(self, completion):
        return completion["choices"][0]["message"].get("tool_calls") or []

    def message_text(self, completion):
        return completion["choices"][0]["message"].get("content") or ""

    def parse_tool_args(self, call):
        return json.loads(call["function"].get("arguments") or "{}")


def test_mock_llm_grounded_flow(monkeypatch):
    monkeypatch.setattr(
        orch,
        "LLMClient",
        lambda: ScriptedLLM(
            "get_player_stats", {"player": "Josh Allen", "season": 2026}, "Josh Allen has 835 passing yards."
        ),
    )
    result = run("How many passing yards does Josh Allen have?", "analyst")
    assert [t["tool"] for t in result["tool_calls"]] == ["get_player_stats"]
    assert result["fallback"] is False
    assert result["sources"]


def test_mock_llm_fabricated_number_falls_back(monkeypatch):
    monkeypatch.setattr(
        orch,
        "LLMClient",
        lambda: ScriptedLLM(
            "get_player_stats", {"player": "Josh Allen", "season": 2026}, "Josh Allen has 900 passing yards."
        ),
    )
    result = run("How many passing yards does Josh Allen have?", "analyst")
    assert result["fallback"] is True
    # Fallback returns raw evidence containing the real value.
    assert "835" in result["answer"]
