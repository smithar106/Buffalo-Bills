"""Read-only agent tools.

Each tool returns structured JSON with `source` and `retrieved_at` metadata.
The LLM selects tools; the tools fetch facts; the model only explains them.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

from fastapi.encoders import jsonable_encoder

from app.providers.news import get_news_provider
from app.providers.sports import get_sports_provider

# Human-readable source labels shown as citations in the UI.
SOURCE_LABELS: dict[str, str] = {
    "get_next_game": "NFL Schedule",
    "get_schedule": "NFL Schedule",
    "get_game": "Game Box Score",
    "get_recent_games": "Recent Results",
    "get_standings": "AFC East Standings",
    "get_roster": "Roster",
    "get_player_stats": "Player Statistics",
    "get_team_stats": "Team Statistics",
    "get_play_by_play": "Play-by-Play",
    "get_injuries": "Injury Report",
    "get_head_to_head": "Head-to-Head History",
    "search_bills_news": "News Search",
    "get_player_game_log": "Player Game Log",
}

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_next_game",
            "description": "Get the Buffalo Bills' next scheduled game.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_schedule",
            "description": "Get the Buffalo Bills' full schedule for a season.",
            "parameters": {
                "type": "object",
                "properties": {"season": {"type": "integer"}},
                "required": ["season"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_game",
            "description": "Get details (score, matchup, location) for a specific game by id.",
            "parameters": {
                "type": "object",
                "properties": {"game_id": {"type": "string"}},
                "required": ["game_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_games",
            "description": "Get the Bills' most recent completed games with scores.",
            "parameters": {
                "type": "object",
                "properties": {"limit": {"type": "integer"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_standings",
            "description": "Get current AFC East division standings.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_roster",
            "description": "Get the Buffalo Bills active roster.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_player_stats",
            "description": "Get season statistics for a specific player (e.g. 'Josh Allen').",
            "parameters": {
                "type": "object",
                "properties": {
                    "player": {"type": "string"},
                    "season": {"type": "integer"},
                },
                "required": ["player", "season"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_team_stats",
            "description": "Get Buffalo Bills team-level statistics for a season.",
            "parameters": {
                "type": "object",
                "properties": {"season": {"type": "integer"}},
                "required": ["season"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_play_by_play",
            "description": "Get the play-by-play for a specific game.",
            "parameters": {
                "type": "object",
                "properties": {"game_id": {"type": "string"}},
                "required": ["game_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_injuries",
            "description": "Get the Bills' current injury report.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_head_to_head",
            "description": "Get head-to-head history vs an opponent (e.g. 'Chiefs').",
            "parameters": {
                "type": "object",
                "properties": {
                    "opponent": {"type": "string"},
                    "start_season": {"type": "integer"},
                    "end_season": {"type": "integer"},
                },
                "required": ["opponent"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_bills_news",
            "description": "Search recent Bills news and reports.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_player_game_log",
            "description": "Get a player's per-game stats for a season.",
            "parameters": {
                "type": "object",
                "properties": {
                    "player": {"type": "string"},
                    "season": {"type": "integer"},
                },
                "required": ["player", "season"],
            },
        },
    },
]


class ToolRunner:
    """Executes tool calls against the sports and news providers."""

    def execute(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        provider = get_sports_provider()
        start = time.monotonic()

        if name == "get_next_game":
            payload = provider.get_next_game()
        elif name == "get_schedule":
            payload = provider.get_schedule(args.get("season", 2026))
        elif name == "get_game":
            try:
                payload = provider.get_game(args["game_id"])
            except KeyError:
                payload = {"error": "game not found"}
        elif name == "get_recent_games":
            payload = provider.get_recent_games(args.get("limit", 5))
        elif name == "get_standings":
            payload = provider.get_standings()
        elif name == "get_roster":
            payload = provider.get_roster()
        elif name == "get_player_stats":
            payload = provider.get_player_stats(args.get("player", ""), args.get("season", 2026))
        elif name == "get_team_stats":
            payload = provider.get_team_stats(args.get("season", 2026))
        elif name == "get_play_by_play":
            payload = provider.get_play_by_play(args.get("game_id", ""))
        elif name == "get_injuries":
            payload = provider.get_injuries()
        elif name == "get_head_to_head":
            payload = provider.get_head_to_head(
                args.get("opponent", ""),
                args.get("start_season", 2018),
                args.get("end_season", 2026),
            )
        elif name == "search_bills_news":
            payload = get_news_provider().search(args.get("query", ""))
        elif name == "get_player_game_log":
            payload = provider.get_player_game_log(args.get("player", ""), args.get("season", 2026))
        else:
            payload = {"error": f"unknown tool {name}"}

        latency_ms = int((time.monotonic() - start) * 1000)

        # News items carry their own retrieved_at; otherwise stamp now.
        retrieved_at = datetime.now(timezone.utc).isoformat()

        return {
            "tool": name,
            "source": SOURCE_LABELS.get(name, name),
            "arguments": args,
            "retrieved_at": retrieved_at,
            "latency_ms": latency_ms,
            "payload": jsonable_encoder(payload),
        }
