"""News provider factory."""

from functools import lru_cache

from app.config import get_settings

from .live import LiveNewsProvider
from .mock import MockNewsProvider


@lru_cache
def get_news_provider():
    settings = get_settings()
    if settings.news_provider.lower() == "live":
        return LiveNewsProvider()
    return MockNewsProvider()
