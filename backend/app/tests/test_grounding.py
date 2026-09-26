"""Tests for the grounding validator."""

from app.agent.grounding import build_fallback_answer, validate_answer


def test_no_evidence_marks_all_numbers_unsupported():
    assert validate_answer("The Bills scored 34 points", []) == ["34"]


def test_supported_numbers_pass():
    evidence = [{"tool": "get_player_stats", "payload": {"passing_yards": 835, "passing_tds": 6}}]
    assert validate_answer("Josh Allen has 835 passing yards and 6 touchdowns", evidence) == []


def test_unsupported_number_flagged():
    evidence = [{"tool": "get_player_stats", "payload": {"passing_yards": 835}}]
    unsupported = validate_answer("Josh Allen has 900 passing yards", evidence)
    assert "900" in unsupported


def test_time_from_iso_timestamp_supported():
    evidence = [{"tool": "get_next_game", "payload": {"kickoff": "2026-10-04T20:15:00Z"}}]
    assert validate_answer("Kickoff is at 20:15 on October 4, 2026", evidence) == []


def test_float_equivalence():
    evidence = [{"tool": "get_team_stats", "payload": {"value": 27.0}}]
    assert validate_answer("They average 27 points per game", evidence) == []


def test_build_fallback_no_evidence():
    assert build_fallback_answer([]) == "I couldn't verify that from the available Bills data."


def test_build_fallback_includes_evidence():
    evidence = [{"tool": "get_next_game", "source": "NFL Schedule", "payload": {"id": "g1"}}]
    fallback = build_fallback_answer(evidence)
    assert "NFL Schedule" in fallback
    assert "g1" in fallback
