"""Bills Mafia AI — FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, news, schedule, stats
from app.config import get_settings

settings = get_settings()

app = FastAPI(title="Bills Mafia AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schedule.router)
app.include_router(stats.router)
app.include_router(news.router)
app.include_router(chat.router)


@app.get("/health")
def health():
    return {"status": "ok", "sports_data_provider": settings.sports_data_provider}
