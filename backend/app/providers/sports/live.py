"""Live sports provider backed by Big Balls Data (BBS).

Maps BBS's NFL surface to the application's normalized pydantic models.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.models import (
    Game,
    HeadToHead,
    Injury,
    Player,
    PlayerGameLogEntry,
    PlayerSeasonStat,
    Play,
    StandingsEntry,
    Team,
    TeamStat,
)

from .bbs import AFC_EAST, BBSClient, NFL_TEAMS

DEFAULT_SEASON = 2026


def _team(abbr: str) -> Team:
    name, conf, div = NFL_TEAMS.get(abbr, (abbr, "", ""))
    return Team(
        id=abbr.lower(),
        name=name,
        abbreviation=abbr,
        city=name.replace(" Bills", "").replace(" Dolphins", ""),
        conference=conf,
        division=div,
    )


def _parse_date(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


class LiveSportsProvider:
    label = "live"

    def __init__(self) -> None:
        self.client = BBSClient()

    def _current_season(self) -> int:
        rows = self.client.standings()
        for r in rows:
            season = r.get("season")
            if season:
                return int(season)
        return DEFAULT_SEASON

    def _kickoff_map(self) -> dict[str, dict]:
        """match_id -> {kickoff_utc, status} from the generic matches surface."""
        try:
            matches = self.client.get(
                "/v1/matches",
                params={"sport": "american_football", "league": "nfl", "limit": 200},
                ttl=300,
            ).get("data", [])
        except Exception:
            return {}
        return {
            m["id"]: {"kickoff_utc": m.get("kickoff_utc"), "status": m.get("status")}
            for m in matches
        }

    def _to_game(self, row: dict, kickoff_map: dict | None = None) -> Game:
        kickoff_map = kickoff_map or {}
        info = kickoff_map.get(row.get("match_id"), {})
        kickoff = info.get("kickoff_utc") or f"{row['game_date']}T00:00:00Z"

        home_score = row.get("home_score")
        away_score = row.get("away_score")
        status = "final" if (home_score is not None and away_score is not None) else "scheduled"
        live_status = info.get("status")
        if live_status == "live":
            status = "live"
        elif live_status == "scheduled" and status == "scheduled":
            status = "scheduled"

        return Game(
            id=row["game_id"],
            season=row.get("season", DEFAULT_SEASON),
            week=row.get("week", 0),
            home_team=_team(row["home_team"]),
            away_team=_team(row["away_team"]),
            status=status,
            kickoff=_parse_date(kickoff),
            venue=row.get("stadium") or "Highmark Stadium",
            location="",
            home_score=home_score,
            away_score=away_score,
            quarter_scores=[],
            source="bigballsdata",
            retrieved_at=datetime.now(timezone.utc),
        )

    def _bills_games(self, season: int | None = None) -> list[Game]:
        season = season or self._current_season()
        rows = self.client.games(season, team="BUF")
        kickoff_map = self._kickoff_map()
        return [self._to_game(r, kickoff_map) for r in rows]

    def get_next_game(self) -> Game:
        games = self._bills_games()
        upcoming = [g for g in games if g.status in ("scheduled", "live")]
        upcoming.sort(key=lambda g: g.kickoff)
        if upcoming:
            return upcoming[0]
        games.sort(key=lambda g: g.kickoff, reverse=True)
        return games[0]

    def get_schedule(self, season: int) -> list[Game]:
        return self._bills_games(season)

    def get_game(self, game_id: str) -> Game:
        row = self.client.game(game_id)
        if not row:
            raise KeyError(f"game {game_id} not found")
        return self._to_game(row, self._kickoff_map())

    def get_recent_games(self, limit: int) -> list[Game]:
        games = [g for g in self._bills_games() if g.status == "final"]
        games.sort(key=lambda g: g.kickoff, reverse=True)
        return games[:limit]

    def get_standings(self) -> list[StandingsEntry]:
        season = self._current_season()
        entries = []
        for row in self.client.standings():
            name = row.get("team_name", "")
            abbr = next((a for a, (n, _, _) in NFL_TEAMS.items() if n == name), None)
            if abbr not in AFC_EAST:
                continue
            entries.append(
                StandingsEntry(
                    team=_team(abbr),
                    wins=int(row.get("wins") or 0),
                    losses=int(row.get("losses") or 0),
                    ties=int(row.get("ties") or 0),
                    win_pct=float(row.get("win_pct") or 0),
                    division_wins=0,
                    division_losses=0,
                    points_for=int(row.get("points_for") or 0),
                    points_against=int(row.get("points_against") or 0),
                    season=season,
                    source="bigballsdata",
                    retrieved_at=datetime.now(timezone.utc),
                )
            )
        entries.sort(key=lambda e: (-e.wins, e.team.abbreviation))
        return entries

    def get_roster(self) -> list[Player]:
        roster = []
        for r in self.client.roster(self._current_season(), "BUF"):
            roster.append(
                Player(
                    id=r.get("player_id") or str(r.get("player_name")),
                    name=r.get("player_name", ""),
                    number=int(r.get("jersey_number") or 0),
                    position=r.get("position", ""),
                    height="",
                    weight=0,
                    college="",
                    experience=int(r.get("years_exp") or 0),
                    source="bigballsdata",
                    retrieved_at=datetime.now(timezone.utc),
                )
            )
        return roster

    def get_player_stats(self, player: str, season: int) -> list[PlayerSeasonStat]:
        player_id = self.client.player_id(player)
        if not player_id:
            return []
        rows = self.client.player_stats(player_id, season)
        if not rows:
            return []

        # Aggregate weekly rows into a season line.
        totals = PlayerSeasonStat(
            player=Player(id=player_id, name=rows[0].get("player_name", player), number=0, position=rows[0].get("position", ""), height="", weight=0, college="", experience=0),
            season=season,
            games_played=len(rows),
            source="bigballsdata",
            retrieved_at=datetime.now(timezone.utc),
        )
        for r in rows:
            totals.passing_yards += int(r.get("passing_yards") or 0)
            totals.passing_tds += int(r.get("passing_tds") or 0)
            totals.interceptions += int(r.get("interceptions_thrown") or 0)
            totals.rushing_yards += int(r.get("rushing_yards") or 0)
            totals.rushing_tds += int(r.get("rushing_tds") or 0)
            totals.receptions += int(r.get("receptions") or 0)
            totals.receiving_yards += int(r.get("receiving_yards") or 0)
            totals.receiving_tds += int(r.get("receiving_tds") or 0)
            totals.tackles += int(r.get("tackles_solo") or 0) + int(r.get("tackle_assists") or 0)
            totals.sacks += float(r.get("sacks") or 0)
            totals.field_goals_made += int(r.get("fg_made") or 0)
            totals.field_goals_attempted += int(r.get("fg_att") or 0)
        return [totals]

    def get_team_stats(self, season: int) -> list[TeamStat]:
        rows = self.client.team_stats(season)
        if not rows:
            return []
        agg: dict[str, float] = {}
        for r in rows:
            for cat, field in (
                ("passing_yards_per_game", ("passing", "yards")),
                ("rushing_yards_per_game", ("rushing", "yards")),
                ("receiving_yards_per_game", ("receiving", "yards")),
            ):
                agg[cat] = agg.get(cat, 0.0) + (r.get(field[0], {}).get(field[1]) or 0)
        weeks = len(rows)
        return [
            TeamStat(season=season, category=cat, value=round(total / max(weeks, 1), 1), rank=0, source="bigballsdata")
            for cat, total in agg.items()
        ]

    def get_play_by_play(self, game_id: str) -> list[Play]:
        # Play-by-play requires the BBS Pro plan; return empty gracefully.
        return []

    def get_injuries(self) -> list[Injury]:
        injuries = []
        for r in self.client.injuries("BUF"):
            status = (r.get("roster", {}) or {}).get("status") or (r.get("practice", {}) or {}).get("status")
            detail = (r.get("report", {}) or {}).get("primary_injury") or (r.get("practice", {}) or {}).get("primary_injury")
            if not status:
                continue
            injuries.append(
                Injury(
                    player=Player(
                        id=r.get("player_id") or f"inj-{r.get('full_name', 'unknown')}",
                        name=r.get("full_name") or "Unknown",
                        number=0,
                        position=r.get("position") or "",
                        height="",
                        weight=0,
                        college="",
                        experience=0,
                    ),
                    status=status,
                    injury=detail or "",
                    updated=datetime.now(timezone.utc),
                    source="bigballsdata",
                    retrieved_at=datetime.now(timezone.utc),
                )
            )
        return injuries

    def get_head_to_head(self, opponent: str, start_season: int, end_season: int) -> HeadToHead:
        opp_abbr = next((a for a, (n, _, _) in NFL_TEAMS.items() if opponent.lower() in n.lower()), None)
        if not opp_abbr:
            opp_abbr = opponent.upper()

        meetings: list[Game] = []
        for season in range(start_season, end_season + 1):
            try:
                rows = self.client.games(season, team="BUF")
            except Exception:
                continue
            for r in rows:
                if r.get("home_team") == opp_abbr or r.get("away_team") == opp_abbr:
                    meetings.append(self._to_game(r))

        a_wins = 0
        b_wins = 0
        for g in meetings:
            if g.status != "final":
                continue
            is_bills_home = g.home_team.abbreviation == "BUF"
            bills_score = g.home_score if is_bills_home else g.away_score
            opp_score = g.away_score if is_bills_home else g.home_score
            if bills_score is not None and opp_score is not None:
                if bills_score > opp_score:
                    a_wins += 1
                elif opp_score > bills_score:
                    b_wins += 1

        return HeadToHead(
            team_a=_team("BUF"),
            team_b=_team(opp_abbr),
            start_season=start_season,
            end_season=end_season,
            meetings=meetings,
            team_a_wins=a_wins,
            team_b_wins=b_wins,
            source="bigballsdata",
            retrieved_at=datetime.now(timezone.utc),
        )

    def get_player_game_log(self, player: str, season: int) -> list[PlayerGameLogEntry]:
        player_id = self.client.player_id(player)
        if not player_id:
            return []
        log = []
        for r in self.client.player_stats(player_id, season):
            log.append(
                PlayerGameLogEntry(
                    game_id=r.get("match_id", ""),
                    season=season,
                    week=int(r.get("week") or 0),
                    opponent="",
                    passing_yards=int(r.get("passing_yards") or 0),
                    passing_tds=int(r.get("passing_tds") or 0),
                    interceptions=int(r.get("interceptions_thrown") or 0),
                    rushing_yards=int(r.get("rushing_yards") or 0),
                    rushing_tds=int(r.get("rushing_tds") or 0),
                    receptions=int(r.get("receptions") or 0),
                    receiving_yards=int(r.get("receiving_yards") or 0),
                    receiving_tds=int(r.get("receiving_tds") or 0),
                    source="bigballsdata",
                    retrieved_at=datetime.now(timezone.utc),
                )
            )
        return log

    def get_historical_games(self, **filters) -> list[Game]:
        season = filters.get("season") or self._current_season()
        return self._bills_games(season)

    def get_game_actual(self, game_id: str) -> dict | None:
        try:
            game = self.get_game(game_id)
        except Exception:
            return None
        if game.status != "final":
            return None
        is_home = game.home_team.abbreviation == "BUF"
        bills_score = game.home_score if is_home else game.away_score
        opp_score = game.away_score if is_home else game.home_score
        return {
            "bills_score": bills_score,
            "opponent_score": opp_score,
            "first_td_scorer": "",
            "allen_passing_yards": 0,
        }
