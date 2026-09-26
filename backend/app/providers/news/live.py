"""Live news provider placeholder."""

from app.models import NewsItem


class LiveNewsProvider:
    label = "live"

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key

    def search(self, query: str, limit: int = 5) -> list[NewsItem]:
        raise NotImplementedError(
            "LiveNewsProvider requires a news API integration. "
            "Set NEWS_PROVIDER=mock for demo mode or implement this adapter."
        )

    def recent(self, limit: int = 5) -> list[NewsItem]:
        raise NotImplementedError(
            "LiveNewsProvider requires a news API integration. "
            "Set NEWS_PROVIDER=mock for demo mode or implement this adapter."
        )
