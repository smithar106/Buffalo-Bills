# Data Providers

## Sports data

The application is decoupled from any single sports API via a provider interface.

```python
class SportsDataProvider(Protocol):
    def get_schedule(self, season: int) -> list[Game]: ...
    def get_game(self, game_id: str) -> Game: ...
    def get_standings(self) -> list[StandingsEntry]: ...
    def get_roster(self) -> list[Player]: ...
    def get_player_stats(self, player: str, season: int) -> list[PlayerStat]: ...
    def get_team_stats(self, season: int) -> list[TeamStat]: ...
    def get_play_by_play(self, game_id: str) -> list[Play]: ...
    def get_injuries(self) -> list[Injury]: ...
    def get_historical_games(self, **filters) -> list[Game]: ...
```

### MockSportsProvider

Deterministic, realistic, **clearly labeled** demo data. Fully usable offline.
No credentials. The UI shows a `DEMO DATA` badge whenever mock mode is active.

### LiveSportsProvider

Structured so a real NFL/sports API can be plugged in later. Configure the
provider in `backend/app/providers/sports/__init__.py` and add any required
credentials to `.env`. When `SPORTS_DATA_PROVIDER=live`, the live adapter is
used; its output is normalized to the same pydantic models as mock.

## News

`NewsProvider` interface with `MockNewsProvider` and `LiveNewsProvider`.

News results contain: `title`, `publisher`, `published_at`, `url`, `summary`.

The agent may summarize news but must distinguish **reported news / analysis**
from **factual sports data** — and must not present article speculation as fact.

## Data freshness

Every structured response carries `source`, `retrieved_at`, `season`, and
`game_id` (where relevant). The UI renders "Updated X minutes ago". Stale data
is never presented as live.
