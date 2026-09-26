"""Schedule and game-related endpoints."""

from fastapi import APIRouter, HTTPException, Query

from app.providers.sports import get_sports_provider

router = APIRouter(prefix="/api", tags=["schedule"])


@router.get("/next-game")
def next_game():
    provider = get_sports_provider()
    game = provider.get_next_game()
    return {
        "game": game,
        "demo": provider.label == "mock",
        "retrieved_at": game.retrieved_at,
    }


@router.get("/schedule")
def schedule(season: int = Query(default=2026)):
    provider = get_sports_provider()
    games = provider.get_schedule(season)
    return {"games": games, "season": season, "demo": provider.label == "mock"}


@router.get("/games/recent")
def recent_games(limit: int = Query(default=5, ge=1, le=25)):
    provider = get_sports_provider()
    return {"games": provider.get_recent_games(limit), "demo": provider.label == "mock"}


@router.get("/games/{game_id}")
def game(game_id: str):
    provider = get_sports_provider()
    try:
        game = provider.get_game(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"game": game, "demo": provider.label == "mock"}


@router.get("/games/{game_id}/plays")
def play_by_play(game_id: str):
    provider = get_sports_provider()
    plays = provider.get_play_by_play(game_id)
    return {"game_id": game_id, "plays": plays, "demo": provider.label == "mock"}


@router.get("/head-to-head")
def head_to_head(
    opponent: str,
    start_season: int = Query(default=2018),
    end_season: int = Query(default=2026),
):
    provider = get_sports_provider()
    return {
        "head_to_head": provider.get_head_to_head(opponent, start_season, end_season),
        "demo": provider.label == "mock",
    }
