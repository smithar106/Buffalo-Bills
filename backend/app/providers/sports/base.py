"""Sports data provider interface."""

from typing import Protocol, runtime_checkable

from app.models import (
    Game,
    HeadToHead,
    Injury,
    PlayerGameLogEntry,
    PlayerSeasonStat,
    Play,
    StandingsEntry,
    TeamStat,
)


@runtime_checkable
class SportsDataProvider(Protocol):
    def get_next_game(self) -> Game: ...

    def get_schedule(self, season: int) -> list[Game]: ...

    def get_game(self, game_id: str) -> Game: ...

    def get_recent_games(self, limit: int) -> list[Game]: ...

    def get_standings(self) -> list[StandingsEntry]: ...

    def get_roster(self) -> list: ...

    def get_player_stats(self, player: str, season: int) -> list[PlayerSeasonStat]: ...

    def get_team_stats(self, season: int) -> list[TeamStat]: ...

    def get_play_by_play(self, game_id: str) -> list[Play]: ...

    def get_injuries(self) -> list[Injury]: ...

    def get_head_to_head(
        self, opponent: str, start_season: int, end_season: int
    ) -> HeadToHead: ...

    def get_player_game_log(self, player: str, season: int) -> list[PlayerGameLogEntry]: ...

    def get_historical_games(self, **filters) -> list[Game]: ...
