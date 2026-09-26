"""Tests for the mock sports provider (deterministic golden facts)."""


def test_next_game_is_chiefs(mock_provider):
    game = mock_provider.get_next_game()
    assert game.status == "scheduled"
    assert "Chiefs" in game.home_team.name or "Chiefs" in game.away_team.name


def test_recent_games_are_final(mock_provider):
    games = mock_provider.get_recent_games(limit=3)
    assert len(games) == 3
    assert all(g.status == "final" for g in games)


def test_schedule_has_entries(mock_provider):
    games = mock_provider.get_schedule(2026)
    assert len(games) >= 8


def test_standings_bills_first(mock_provider):
    standings = mock_provider.get_standings()
    bills = [s for s in standings if s.team.abbreviation == "BUF"][0]
    assert bills.wins == 3
    assert bills.losses == 0


def test_josh_allen_stats(mock_provider):
    stats = mock_provider.get_player_stats("Josh Allen", 2026)
    assert len(stats) == 1
    s = stats[0]
    assert s.passing_yards == 835
    assert s.passing_tds == 6
    assert s.interceptions == 1


def test_game_log_deterministic(mock_provider):
    log = mock_provider.get_player_game_log("Josh Allen", 2026)
    assert len(log) == 3
    assert log[0].passing_yards == 285


def test_roster_includes_allen(mock_provider):
    roster = mock_provider.get_roster()
    names = [p.name.lower() for p in roster]
    assert "josh allen" in names


def test_injuries_present(mock_provider):
    injuries = mock_provider.get_injuries()
    assert len(injuries) >= 1


def test_head_to_head_chiefs(mock_provider):
    h2h = mock_provider.get_head_to_head("Chiefs", 2022, 2026)
    assert h2h.team_b.abbreviation == "KC"
    assert h2h.meetings


def test_play_by_play_game1(mock_provider):
    plays = mock_provider.get_play_by_play("2026-w1-buf-nyj")
    assert len(plays) == 5
    assert plays[0].points == 7
