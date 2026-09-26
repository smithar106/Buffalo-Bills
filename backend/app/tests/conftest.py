import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


@pytest.fixture(autouse=True)
def _reset_provider_to_mock(monkeypatch):
    """Ensure every test starts with the mock provider and clean caches."""
    from app.config import get_settings
    from app.providers.news import get_news_provider
    from app.providers.sports import get_sports_provider

    monkeypatch.setenv("SPORTS_DATA_PROVIDER", "mock")
    monkeypatch.setenv("NEWS_PROVIDER", "mock")
    get_settings.cache_clear()
    get_sports_provider.cache_clear()
    get_news_provider.cache_clear()
    yield
    get_settings.cache_clear()
    get_sports_provider.cache_clear()
    get_news_provider.cache_clear()


@pytest.fixture
def mock_provider():
    from app.providers.sports import get_sports_provider

    return get_sports_provider()
