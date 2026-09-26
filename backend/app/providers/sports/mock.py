"""Mock sports provider.

Deterministic, clearly-labeled demo data. No external API credentials required.
"""

from datetime import datetime, timedelta, timezone

from app.models import (
    Game,
    HeadToHead,
    Injury,
    Player,
    PlayerGameLogEntry,
    PlayerSeasonStat,
    Play,
    QuarterScore,
    StandingsEntry,
    Team,
    TeamStat,
)

MOCK_SEASON = 2026
CURRENT_WEEK = 4  # games 1-3 are final, week 4 is the next game

BILLS = Team(
    id="buf",
    name="Buffalo Bills",
    abbreviation="BUF",
    city="Buffalo",
    conference="AFC",
    division="AFC East",
)
DOLPHINS = Team(
    id="mia",
    name="Miami Dolphins",
    abbreviation="MIA",
    city="Miami",
    conference="AFC",
    division="AFC East",
)
PATRIOTS = Team(
    id="ne",
    name="New England Patriots",
    abbreviation="NE",
    city="New England",
    conference="AFC",
    division="AFC East",
)
JETS = Team(
    id="nyj",
    name="New York Jets",
    abbreviation="NYJ",
    city="New York",
    conference="AFC",
    division="AFC East",
)
CHIEFS = Team(
    id="kc",
    name="Kansas City Chiefs",
    abbreviation="KC",
    city="Kansas City",
    conference="AFC",
    division="AFC West",
)
TITANS = Team(
    id="ten",
    name="Tennessee Titans",
    abbreviation="TEN",
    city="Nashville",
    conference="AFC",
    division="AFC South",
)
RAVENS = Team(
    id="bal",
    name="Baltimore Ravens",
    abbreviation="BAL",
    city="Baltimore",
    conference="AFC",
    division="AFC North",
)
RAIDERS = Team(
    id="lv",
    name="Las Vegas Raiders",
    abbreviation="LV",
    city="Las Vegas",
    conference="AFC",
    division="AFC West",
)

TEAMS = [BILLS, DOLPHINS, PATRIOTS, JETS, CHIEFS, TITANS, RAVENS, RAIDERS]

ROSTER = [
    Player(id="p_allen", name="Josh Allen", number=17, position="QB", height="6'5\"", weight=237, college="Wyoming", experience=9),
    Player(id="p_cook", name="James Cook", number=4, position="RB", height="5'11\"", weight=190, college="Georgia", experience=5),
    Player(id="p_shakir", name="Khalil Shakir", number=10, position="WR", height="6'0\"", weight=190, college="Boise State", experience=5),
    Player(id="p_coleman", name="Keon Coleman", number=0, position="WR", height="6'4\"", weight=215, college="Florida State", experience=4),
    Player(id="p_kincaid", name="Dalton Kincaid", number=86, position="TE", height="6'4\"", weight=240, college="Utah", experience=4),
    Player(id="p_samuel", name="Curtis Samuel", number=1, position="WR", height="5'11\"", weight=195, college="Ohio State", experience=10),
    Player(id="p_knox", name="Dawson Knox", number=88, position="TE", height="6'4\"", weight=254, college="Ole Miss", experience=8),
    Player(id="p_bass", name="Tyler Bass", number=2, position="K", height="5'10\"", weight=183, college="Georgia Southern", experience=7),
    Player(id="p_bernard", name="Terrel Bernard", number=43, position="LB", height="6'1\"", weight=224, college="Baylor", experience=5),
    Player(id="p_rousseau", name="Greg Rousseau", number=50, position="DE", height="6'7\"", weight=266, college="Miami", experience=6),
    Player(id="p_johnson", name="Taron Johnson", number=7, position="CB", height="5'11\"", weight=192, college="Weber State", experience=9),
    Player(id="p_oliver", name="Ed Oliver", number=91, position="DT", height="6'1\"", weight=287, college="Houston", experience=8),
]

PLAYER_BY_NAME = {p.name.lower(): p for p in ROSTER}


def _kickoff(week: int, day_offset: int = 0) -> datetime:
    # Fixed anchor for deterministic mock data: season kickoff Thu Sep 10 2026.
    anchor = datetime(2026, 9, 10, 20, 15, tzinfo=timezone.utc)
    return anchor + timedelta(weeks=week - 1, days=day_offset)


def _game(
    gid: str,
    week: int,
    home: Team,
    away: Team,
    status: str,
    home_score=None,
    away_score=None,
    quarters=None,
    venue="Highmark Stadium",
    location="Orchard Park, NY",
    day_offset=0,
    season=None,
) -> Game:
    return Game(
        id=gid,
        season=MOCK_SEASON if season is None else season,
        week=week,
        home_team=home,
        away_team=away,
        status=status,
        kickoff=_kickoff(week, day_offset),
        venue=venue,
        location=location,
        home_score=home_score,
        away_score=away_score,
        quarter_scores=quarters or [],
        source="mock",
    )


SCHEDULE = [
    _game("2026-w1-buf-nyj", 1, JETS, BILLS, "final", 17, 34,
          [QuarterScore(quarter=1, home=0, away=7), QuarterScore(quarter=2, home=10, away=14),
           QuarterScore(quarter=3, home=7, away=6), QuarterScore(quarter=4, home=0, away=7)],
          venue="MetLife Stadium", location="East Rutherford, NJ"),
    _game("2026-w2-mia-buf", 2, BILLS, DOLPHINS, "final", 27, 24,
          [QuarterScore(quarter=1, home=7, away=3), QuarterScore(quarter=2, home=10, away=7),
           QuarterScore(quarter=3, home=3, away=7), QuarterScore(quarter=4, home=7, away=7)]),
    _game("2026-w3-buf-ne", 3, PATRIOTS, BILLS, "final", 10, 20,
          [QuarterScore(quarter=1, home=3, away=7), QuarterScore(quarter=2, home=0, away=3),
           QuarterScore(quarter=3, home=7, away=7), QuarterScore(quarter=4, home=0, away=3)],
          venue="Gillette Stadium", location="Foxborough, MA"),
    _game("2026-w4-kc-buf", 4, BILLS, CHIEFS, "scheduled", venue="Highmark Stadium", location="Orchard Park, NY", day_offset=3),
    _game("2026-w5-buf-ten", 5, TITANS, BILLS, "scheduled", venue="Nissan Stadium", location="Nashville, TN"),
    _game("2026-w6-nyj-buf", 6, BILLS, JETS, "scheduled"),
    _game("2026-w7-buf-lv", 7, RAIDERS, BILLS, "scheduled", venue="Allegiant Stadium", location="Las Vegas, NV"),
    _game("2026-w9-ne-buf", 9, BILLS, PATRIOTS, "scheduled"),
    _game("2026-w11-mia-buf", 11, BILLS, DOLPHINS, "scheduled"),
    _game("2026-w12-buf-bal", 12, RAVENS, BILLS, "scheduled", venue="M&T Bank Stadium", location="Baltimore, MD"),
    _game("2026-w17-ne-buf", 17, BILLS, PATRIOTS, "scheduled"),
    _game("2026-w18-buf-mia", 18, DOLPHINS, BILLS, "scheduled", venue="Hard Rock Stadium", location="Miami Gardens, FL"),
]

STANDINGS = [
    StandingsEntry(team=BILLS, wins=3, losses=0, ties=0, win_pct=1.0, division_wins=2, division_losses=0, points_for=81, points_against=51, season=MOCK_SEASON),
    StandingsEntry(team=DOLPHINS, wins=2, losses=1, ties=0, win_pct=0.667, division_wins=1, division_losses=1, points_for=72, points_against=58, season=MOCK_SEASON),
    StandingsEntry(team=PATRIOTS, wins=1, losses=2, ties=0, win_pct=0.333, division_wins=0, division_losses=2, points_for=45, points_against=63, season=MOCK_SEASON),
    StandingsEntry(team=JETS, wins=0, losses=3, ties=0, win_pct=0.0, division_wins=0, division_losses=1, points_for=38, points_against=72, season=MOCK_SEASON),
]

ALLEN_GAME_LOG = [
    PlayerGameLogEntry(game_id="2026-w1-buf-nyj", season=MOCK_SEASON, week=1, opponent="Jets", passing_yards=285, passing_tds=2, interceptions=0, rushing_yards=45, rushing_tds=1),
    PlayerGameLogEntry(game_id="2026-w2-mia-buf", season=MOCK_SEASON, week=2, opponent="Dolphins", passing_yards=310, passing_tds=3, interceptions=1, rushing_yards=25, rushing_tds=0),
    PlayerGameLogEntry(game_id="2026-w3-buf-ne", season=MOCK_SEASON, week=3, opponent="Patriots", passing_yards=240, passing_tds=1, interceptions=0, rushing_yards=35, rushing_tds=1),
]

PLAYER_STATS = {
    "josh allen": PlayerSeasonStat(
        player=PLAYER_BY_NAME["josh allen"], season=MOCK_SEASON, games_played=3,
        passing_yards=835, passing_tds=6, interceptions=1, rushing_yards=105, rushing_tds=2,
    ),
    "james cook": PlayerSeasonStat(
        player=PLAYER_BY_NAME["james cook"], season=MOCK_SEASON, games_played=3,
        rushing_yards=285, rushing_tds=3, receptions=9, receiving_yards=74, receiving_tds=0,
    ),
    "khalil shakir": PlayerSeasonStat(
        player=PLAYER_BY_NAME["khalil shakir"], season=MOCK_SEASON, games_played=3,
        receptions=22, receiving_yards=280, receiving_tds=2,
    ),
    "keon coleman": PlayerSeasonStat(
        player=PLAYER_BY_NAME["keon coleman"], season=MOCK_SEASON, games_played=3,
        receptions=14, receiving_yards=210, receiving_tds=3,
    ),
    "dalton kincaid": PlayerSeasonStat(
        player=PLAYER_BY_NAME["dalton kincaid"], season=MOCK_SEASON, games_played=3,
        receptions=18, receiving_yards=205, receiving_tds=1,
    ),
    "greg rousseau": PlayerSeasonStat(
        player=PLAYER_BY_NAME["greg rousseau"], season=MOCK_SEASON, games_played=3,
        tackles=12, sacks=3.0,
    ),
    "terrel bernard": PlayerSeasonStat(
        player=PLAYER_BY_NAME["terrel bernard"], season=MOCK_SEASON, games_played=3,
        tackles=28, sacks=1.0,
    ),
    "tyler bass": PlayerSeasonStat(
        player=PLAYER_BY_NAME["tyler bass"], season=MOCK_SEASON, games_played=3,
        field_goals_made=7, field_goals_attempted=8,
    ),
}

TEAM_STATS = [
    TeamStat(season=MOCK_SEASON, category="points_per_game", value=27.0, rank=6),
    TeamStat(season=MOCK_SEASON, category="points_allowed_per_game", value=17.0, rank=4),
    TeamStat(season=MOCK_SEASON, category="passing_yards_per_game", value=278.3, rank=7),
    TeamStat(season=MOCK_SEASON, category="rushing_yards_per_game", value=122.0, rank=12),
    TeamStat(season=MOCK_SEASON, category="total_yards_per_game", value=400.3, rank=5),
]

INJURIES = [
    Injury(player=PLAYER_BY_NAME["curtis samuel"], status="Questionable", injury="Hamstring", updated=datetime(2026, 9, 25, 16, 0, tzinfo=timezone.utc)),
    Injury(player=PLAYER_BY_NAME["ed oliver"], status="Out", injury="Ankle", updated=datetime(2026, 9, 24, 14, 30, tzinfo=timezone.utc)),
]

PLAYS_GAME1 = [
    Play(game_id="2026-w1-buf-nyj", play_id="p1", quarter=1, time="13:12", down=3, yards_to_go=7, description="Josh Allen 9-yard touchdown run", offense="BUF", points=7),
    Play(game_id="2026-w1-buf-nyj", play_id="p2", quarter=2, time="9:44", down=2, yards_to_go=5, description="Allen 28-yard TD pass to Keon Coleman", offense="BUF", points=7),
    Play(game_id="2026-w1-buf-nyj", play_id="p3", quarter=2, time="0:02", down=1, yards_to_go=10, description="Tyler Bass 42-yard field goal", offense="BUF", points=3),
    Play(game_id="2026-w1-buf-nyj", play_id="p4", quarter=3, time="6:30", down=2, yards_to_go=3, description="Allen 4-yard TD pass to Dalton Kincaid", offense="BUF", points=7),
    Play(game_id="2026-w1-buf-nyj", play_id="p5", quarter=4, time="11:20", down=1, yards_to_go=10, description="James Cook 12-yard TD run", offense="BUF", points=7),
]

H2H_CHIEFS = [
    _game("2024-w11-buf-kc", 11, BILLS, CHIEFS, "final", 30, 21, venue="Highmark Stadium", location="Orchard Park, NY", day_offset=0, season=2024),
    _game("2023-w14-kc-buf", 14, CHIEFS, BILLS, "final", 20, 17, venue="Arrowhead Stadium", location="Kansas City, MO", day_offset=1, season=2023),
    _game("2023-post-kc-buf", 19, BILLS, CHIEFS, "final", 24, 27, venue="Highmark Stadium", location="Orchard Park, NY", day_offset=2, season=2023),
    _game("2022-w6-buf-kc", 6, CHIEFS, BILLS, "final", 24, 20, venue="Arrowhead Stadium", location="Kansas City, MO", day_offset=3, season=2022),
]

H2H_DOLPHINS = [
    _game("2026-w2-mia-buf", 2, BILLS, DOLPHINS, "final", 27, 24, season=2026),
    _game("2025-w9-mia-buf", 9, BILLS, DOLPHINS, "final", 31, 10, season=2025),
    _game("2024-w2-mia-buf", 2, DOLPHINS, BILLS, "final", 10, 31, venue="Hard Rock Stadium", location="Miami Gardens, FL", season=2024),
]

GAME_ACTUALS = {
    "2026-w1-buf-nyj": {
        "bills_score": 34,
        "opponent_score": 17,
        "first_td_scorer": "Josh Allen",
        "allen_passing_yards": 285,
    },
    "2026-w2-mia-buf": {
        "bills_score": 27,
        "opponent_score": 24,
        "first_td_scorer": "Khalil Shakir",
        "allen_passing_yards": 310,
    },
    "2026-w3-buf-ne": {
        "bills_score": 20,
        "opponent_score": 10,
        "first_td_scorer": "James Cook",
        "allen_passing_yards": 240,
    },
}


class MockSportsProvider:
    """Deterministic, clearly-labeled demo data provider."""

    label = "mock"

    def get_next_game(self) -> Game:
        return SCHEDULE[CURRENT_WEEK - 1]

    def get_schedule(self, season: int) -> list[Game]:
        return [g for g in SCHEDULE if g.season == season]

    def get_game(self, game_id: str) -> Game:
        for g in SCHEDULE:
            if g.id == game_id:
                return g
        raise KeyError(f"game {game_id} not found")

    def get_recent_games(self, limit: int) -> list[Game]:
        final = [g for g in SCHEDULE if g.status == "final"]
        final.sort(key=lambda g: g.kickoff, reverse=True)
        return final[:limit]

    def get_standings(self) -> list[StandingsEntry]:
        return STANDINGS

    def get_roster(self) -> list[Player]:
        return ROSTER

    def get_player_stats(self, player: str, season: int) -> list[PlayerSeasonStat]:
        key = player.lower()
        stat = PLAYER_STATS.get(key)
        if stat is None or stat.season != season:
            return []
        return [stat]

    def get_team_stats(self, season: int) -> list[TeamStat]:
        return [t for t in TEAM_STATS if t.season == season]

    def get_play_by_play(self, game_id: str) -> list[Play]:
        if game_id == "2026-w1-buf-nyj":
            return PLAYS_GAME1
        return []

    def get_injuries(self) -> list[Injury]:
        return INJURIES

    def get_head_to_head(self, opponent: str, start_season: int, end_season: int) -> HeadToHead:
        opp = opponent.lower()
        if opp in ("chiefs", "kansas city", "kc"):
            meetings = H2H_CHIEFS
            other = CHIEFS
        elif opp in ("dolphins", "miami", "mia"):
            meetings = H2H_DOLPHINS
            other = DOLPHINS
        else:
            meetings = []
            other = None

        a_wins = 0
        b_wins = 0
        for g in meetings:
            if g.status != "final":
                continue
            bills_score = g.home_score if g.home_team.id == "buf" else g.away_score
            opp_score = g.away_score if g.home_team.id == "buf" else g.home_score
            if bills_score > opp_score:
                a_wins += 1
            elif opp_score > bills_score:
                b_wins += 1

        team_b = other if other is not None else Team(
            id="unknown", name=opponent, abbreviation=opponent[:3].upper(), city="", conference="", division=""
        )
        return HeadToHead(
            team_a=BILLS, team_b=team_b, start_season=start_season, end_season=end_season,
            meetings=meetings, team_a_wins=a_wins, team_b_wins=b_wins,
        )

    def get_player_game_log(self, player: str, season: int) -> list[PlayerGameLogEntry]:
        if player.lower() == "josh allen" and season == MOCK_SEASON:
            return ALLEN_GAME_LOG
        return []

    def get_historical_games(self, **filters) -> list[Game]:
        season = filters.get("season")
        opponent = filters.get("opponent")
        result = []
        for g in SCHEDULE:
            if season is not None and g.season != season:
                continue
            result.append(g)
        if opponent:
            opp = opponent.lower()
            result = [g for g in result if opp in g.home_team.name.lower() or opp in g.away_team.name.lower()]
        return result

    def get_game_actual(self, game_id: str) -> dict | None:
        return GAME_ACTUALS.get(game_id)
