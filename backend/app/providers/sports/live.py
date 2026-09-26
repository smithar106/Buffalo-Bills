"""Live sports provider.

Placeholder structured so a real NFL/sports API can be plugged in later.
See docs/DATA_PROVIDERS.md for configuration guidance.
"""

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


class LiveSportsProvider:
    """Adapter for a real sports data API.

    Configure the provider here and add required credentials to .env.
    All methods must return the same normalized pydantic models as the mock
    provider so the rest of the application is unaffected by the switch.
    """

    label = "live"

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self._api_key = api_key
        self._base_url = base_url

    def _not_implemented(self) -> None:
        raise NotImplementedError(
            "LiveSportsProvider requires a real sports API integration. "
            "Set SPORTS_DATA_PROVIDER=mock for demo mode or implement this adapter."
        )

    def get_next_game(self) -> Game:
        self._not_implemented()

    def get_schedule(self, season: int) -> list[Game]:
        self._not_implemented()

    def get_game(self, game_id: str) -> Game:
        self._not_implemented()

    def get_recent_games(self, limit: int) -> list[Game]:
        self._not_implemented()

    def get_standings(self) -> list[StandingsEntry]:
        self._not_implemented()

    def get_roster(self) -> list:
        self._not_implemented()

    def get_player_stats(self, player: str, season: int) -> list[PlayerSeasonStat]:
        self._not_implemented()

    def get_team_stats(self, season: int) -> list[TeamStat]:
        self._not_implemented()

    def get_play_by_play(self, game_id: str) -> list[Play]:
        self._not_implemented()

    def get_injuries(self) -> list[Injury]:
        self._not_implemented()

    def get_head_to_head(
        self, opponent: str, start_season: int, end_season: int
    ) -> HeadToHead:
        self._not_implemented()

    def get_player_game_log(self, player: str, season: int) -> list[PlayerGameLogEntry]:
        self._not_implemented()

    def get_historical_games(self, **filters) -> list[Game]:
        self._not_implemented()
