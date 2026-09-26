"""News endpoints."""

from fastapi import APIRouter, Query

from app.providers.news import get_news_provider

router = APIRouter(prefix="/api", tags=["news"])


@router.get("/news")
def news(limit: int = Query(default=5, ge=1, le=20)):
    provider = get_news_provider()
    return {"news": provider.recent(limit), "demo": provider.label == "mock"}


@router.get("/news/search")
def search_news(query: str, limit: int = Query(default=5, ge=1, le=20)):
    provider = get_news_provider()
    return {"news": provider.search(query, limit), "demo": provider.label == "mock"}
