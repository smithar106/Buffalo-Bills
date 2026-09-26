"""Failure-mode tests: unavailable providers and LLM."""

from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


def test_sports_provider_unavailable_returns_503(monkeypatch):
    from app.providers.sports import get_sports_provider

    get_settings.cache_clear()
    get_sports_provider.cache_clear()
    monkeypatch.setenv("SPORTS_DATA_PROVIDER", "live")
    get_settings.cache_clear()

    client = TestClient(app)
    resp = client.get("/api/next-game")
    assert resp.status_code == 503

    get_settings.cache_clear()
    get_sports_provider.cache_clear()
    monkeypatch.setenv("SPORTS_DATA_PROVIDER", "mock")
    get_settings.cache_clear()


def test_news_provider_unavailable_returns_503(monkeypatch):
    from app.providers.news import get_news_provider

    get_settings.cache_clear()
    get_news_provider.cache_clear()
    monkeypatch.setenv("NEWS_PROVIDER", "live")
    get_settings.cache_clear()

    client = TestClient(app)
    resp = client.get("/api/news")
    assert resp.status_code == 503

    get_settings.cache_clear()
    get_news_provider.cache_clear()
    monkeypatch.setenv("NEWS_PROVIDER", "mock")
    get_settings.cache_clear()
