"""Sports provider factory."""

from functools import lru_cache

from app.config import get_settings

from .base import SportsDataProvider
from .live import LiveSportsProvider
from .mock import MockSportsProvider


@lru_cache
def get_sports_provider() -> SportsDataProvider:
    settings = get_settings()
    if settings.sports_data_provider.lower() == "live":
        return LiveSportsProvider()
    return MockSportsProvider()
