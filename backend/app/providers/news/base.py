"""News provider interface."""

from typing import Protocol

from app.models import NewsItem


class NewsProvider(Protocol):
    def search(self, query: str, limit: int = 5) -> list[NewsItem]: ...

    def recent(self, limit: int = 5) -> list[NewsItem]: ...
