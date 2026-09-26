"""Tests for agent tool schemas and the tool runner."""

from app.agent.tools import TOOL_SCHEMAS, ToolRunner


def test_tool_schemas_are_valid():
    names = [t["function"]["name"] for t in TOOL_SCHEMAS]
    expected = {
        "get_next_game",
        "get_schedule",
        "get_game",
        "get_recent_games",
        "get_standings",
        "get_roster",
        "get_player_stats",
        "get_team_stats",
        "get_play_by_play",
        "get_injuries",
        "get_head_to_head",
        "search_bills_news",
        "get_player_game_log",
    }
    assert set(names) == expected


def test_tool_schemas_have_parameters():
    for t in TOOL_SCHEMAS:
        assert t["type"] == "function"
        assert "parameters" in t["function"]


def test_runner_get_next_game_returns_metadata():
    runner = ToolRunner()
    result = runner.execute("get_next_game", {})
    assert result["tool"] == "get_next_game"
    assert result["source"] == "NFL Schedule"
    assert "retrieved_at" in result
    assert result["payload"]["status"] == "scheduled"


def test_runner_standings():
    runner = ToolRunner()
    result = runner.execute("get_standings", {})
    bills = [s for s in result["payload"] if s["team"]["abbreviation"] == "BUF"][0]
    assert bills["wins"] == 3


def test_runner_unknown_tool():
    runner = ToolRunner()
    result = runner.execute("nope", {})
    assert result["payload"] == {"error": "unknown tool nope"}


def test_runner_player_stats_missing():
    runner = ToolRunner()
    result = runner.execute("get_player_stats", {"player": "Nobody", "season": 1999})
    assert result["payload"] == []
