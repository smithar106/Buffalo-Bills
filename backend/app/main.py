"""Bills Mafia AI — FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import chat, news, predictions, schedule, stats
from app.config import get_settings
from app.db.models import Base
from app.db.session import engine, is_sqlite

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # For local demo (SQLite), ensure tables exist. Production (PostgreSQL)
    # uses Alembic migrations via the Railway start command.
    if is_sqlite:
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Bills Mafia AI", version="0.1.0", lifespan=lifespan)

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
app.include_router(predictions.router)


@app.exception_handler(NotImplementedError)
async def provider_not_available(request: Request, exc: NotImplementedError):
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Data provider not available. "
            "Set SPORTS_DATA_PROVIDER=mock / NEWS_PROVIDER=mock or configure a live provider."
        },
    )


@app.get("/health")
def health():
    return {"status": "ok", "sports_data_provider": settings.sports_data_provider}
