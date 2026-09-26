"""Roster, statistics, standings, and injury endpoints."""

from fastapi import APIRouter, Query

from app.providers.sports import get_sports_provider

router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/standings")
def standings():
    provider = get_sports_provider()
    return {"standings": provider.get_standings(), "demo": provider.label == "mock"}


@router.get("/roster")
def roster():
    provider = get_sports_provider()
    return {"roster": provider.get_roster(), "demo": provider.label == "mock"}


@router.get("/stats/team")
def team_stats(season: int = Query(default=2026)):
    provider = get_sports_provider()
    return {"stats": provider.get_team_stats(season), "season": season, "demo": provider.label == "mock"}


@router.get("/stats/player")
def player_stats(player: str, season: int = Query(default=2026)):
    provider = get_sports_provider()
    return {
        "player": player,
        "stats": provider.get_player_stats(player, season),
        "demo": provider.label == "mock",
    }


@router.get("/stats/player/{player}/game-log")
def player_game_log(player: str, season: int = Query(default=2026)):
    provider = get_sports_provider()
    return {
        "player": player,
        "game_log": provider.get_player_game_log(player, season),
        "demo": provider.label == "mock",
    }


@router.get("/injuries")
def injuries():
    provider = get_sports_provider()
    return {"injuries": provider.get_injuries(), "demo": provider.label == "mock"}
