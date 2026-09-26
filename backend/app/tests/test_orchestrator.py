"""Tests for the agent orchestrator (non-LLM paths)."""

from app.agent import run


def test_run_without_llm_returns_fallback(monkeypatch):
    # Force an unconfigured LLM by clearing the API key via settings.
    from app.config import get_settings

    get_settings.cache_clear()
    monkeypatch.setenv("LLM_API_KEY", "")
    monkeypatch.setenv("LLM_BASE_URL", "")
    monkeypatch.setenv("LLM_MODEL", "")
    get_settings.cache_clear()

    result = run("Who do the Bills play next?")
    assert result["fallback"] is True
    assert result["answer"] == "I couldn't verify that from the available Bills data."
    assert result["validation"]["result"] == "no_llm"
    get_settings.cache_clear()
