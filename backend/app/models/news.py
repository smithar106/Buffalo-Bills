"""Normalized news data model."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    id: str
    title: str
    publisher: str
    published_at: datetime
    url: str
    summary: str
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
