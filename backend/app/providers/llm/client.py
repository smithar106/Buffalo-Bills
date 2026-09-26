"""OpenAI-compatible LLM client with tool calling.

Provider-agnostic: configured via LLM_API_KEY, LLM_BASE_URL, LLM_MODEL.
"""

from __future__ import annotations

import json
import time
from typing import Any

import httpx

from app.config import get_settings


class LLMError(RuntimeError):
    pass


class LLMClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.llm_api_key
        self.base_url = settings.llm_base_url.rstrip("/") if settings.llm_base_url else "https://api.openai.com/v1"
        self.model = settings.llm_model or "gpt-4o-mini"

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        *,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> dict[str, Any]:
        if not self.configured:
            raise LLMError("LLM not configured. Set LLM_API_KEY, LLM_BASE_URL, LLM_MODEL.")

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        start = time.monotonic()
        try:
            with httpx.Client(timeout=60) as client:
                resp = client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMError(f"LLM request failed: {exc}") from exc

        latency_ms = int((time.monotonic() - start) * 1000)
        data = resp.json()
        data["_latency_ms"] = latency_ms
        return data

    @staticmethod
    def message_text(completion: dict[str, Any]) -> str:
        choice = completion["choices"][0]
        return choice["message"].get("content") or ""

    @staticmethod
    def tool_calls(completion: dict[str, Any]) -> list[dict[str, Any]]:
        choice = completion["choices"][0]
        return choice["message"].get("tool_calls") or []

    @staticmethod
    def usage(completion: dict[str, Any]) -> dict[str, int] | None:
        return completion.get("usage")

    @staticmethod
    def parse_tool_args(call: dict[str, Any]) -> dict[str, Any]:
        raw = call["function"].get("arguments") or "{}"
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
