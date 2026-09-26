"""Big Balls Data (BBS) HTTP client with a small TTL cache.

REST base: https://api.bigballsdata.com
Auth:      Authorization: Bearer <BBS_API_KEY>
"""

from __future__ import annotations

import time
from typing import Any

import httpx

from app.config import get_settings

# NFL team reference: abbreviation -> (name, conference, division).
NFL_TEAMS: dict[str, tuple[str, str, str]] = {
    "BUF": ("Buffalo Bills", "AFC", "AFC East"),
    "MIA": ("Miami Dolphins", "AFC", "AFC East"),
    "NE": ("New England Patriots", "AFC", "AFC East"),
    "NYJ": ("New York Jets", "AFC", "AFC East"),
    "BAL": ("Baltimore Ravens", "AFC", "AFC North"),
    "CIN": ("Cincinnati Bengals", "AFC", "AFC North"),
    "CLE": ("Cleveland Browns", "AFC", "AFC North"),
    "PIT": ("Pittsburgh Steelers", "AFC", "AFC North"),
    "HOU": ("Houston Texans", "AFC", "AFC South"),
    "IND": ("Indianapolis Colts", "AFC", "AFC South"),
    "JAX": ("Jacksonville Jaguars", "AFC", "AFC South"),
    "TEN": ("Tennessee Titans", "AFC", "AFC South"),
    "DEN": ("Denver Broncos", "AFC", "AFC West"),
    "KC": ("Kansas City Chiefs", "AFC", "AFC West"),
    "LV": ("Las Vegas Raiders", "AFC", "AFC West"),
    "LAC": ("Los Angeles Chargers", "AFC", "AFC West"),
    "DAL": ("Dallas Cowboys", "NFC", "NFC East"),
    "NYG": ("New York Giants", "NFC", "NFC East"),
    "PHI": ("Philadelphia Eagles", "NFC", "NFC East"),
    "WAS": ("Washington Commanders", "NFC", "NFC East"),
    "CHI": ("Chicago Bears", "NFC", "NFC North"),
    "DET": ("Detroit Lions", "NFC", "NFC North"),
    "GB": ("Green Bay Packers", "NFC", "NFC North"),
    "MIN": ("Minnesota Vikings", "NFC", "NFC North"),
    "ATL": ("Atlanta Falcons", "NFC", "NFC South"),
    "CAR": ("Carolina Panthers", "NFC", "NFC South"),
    "NO": ("New Orleans Saints", "NFC", "NFC South"),
    "TB": ("Tampa Bay Buccaneers", "NFC", "NFC South"),
    "ARI": ("Arizona Cardinals", "NFC", "NFC West"),
    "LAR": ("Los Angeles Rams", "NFC", "NFC West"),
    "SF": ("San Francisco 49ers", "NFC", "NFC West"),
    "SEA": ("Seattle Seahawks", "NFC", "NFC West"),
}

AFC_EAST = ("BUF", "MIA", "NE", "NYJ")


class BBSError(RuntimeError):
    pass


class BBSClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.bbs_api_key
        self.base_url = settings.bbs_base_url.rstrip("/")
        self._cache: dict[str, tuple[float, Any]] = {}

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def get(self, path: str, params: dict[str, Any] | None = None, ttl: float = 60.0) -> Any:
        if not self.configured:
            raise BBSError("BBS_API_KEY not configured")

        cache_key = path + "?" + "&".join(f"{k}={v}" for k, v in sorted((params or {}).items()))
        hit = self._cache.get(cache_key)
        if hit and time.monotonic() - hit[0] < ttl:
            return hit[1]

        url = f"{self.base_url}{path}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            with httpx.Client(timeout=30) as client:
                resp = client.get(url, params=params, headers=headers)
        except httpx.HTTPError as exc:
            raise BBSError(f"BBS request failed: {exc}") from exc

        if resp.status_code == 401 or resp.status_code == 403:
            raise BBSError(f"BBS auth failed ({resp.status_code}): {resp.text[:200]}")
        if resp.status_code >= 400:
            raise BBSError(f"BBS error {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        self._cache[cache_key] = (time.monotonic(), data)
        return data

    # --- high-level data access ---

    def games(self, season: int, team: str | None = None) -> list[dict]:
        params: dict[str, Any] = {"season": season}
        if team:
            params["team"] = team
        data = self.get("/v1/nfl/games", params=params, ttl=300)
        return data.get("data", [])

    def game(self, game_id: str) -> dict:
        data = self.get(f"/v1/nfl/games/{game_id}", ttl=300)
        return data.get("data", {})

    def standings(self) -> list[dict]:
        data = self.get("/v1/standings", params={"league": "nfl"}, ttl=300)
        for s in data.get("data", {}).get("standings", []):
            if s.get("league_name") == "NFL":
                return s.get("rows", [])
        return []

    def roster(self, season: int, team: str = "BUF") -> list[dict]:
        data = self.get("/v1/nfl/rosters", params={"season": season, "team": team}, ttl=86400)
        return data.get("data", [])

    def injuries(self, team: str | None = None) -> list[dict]:
        data = self.get("/v1/nfl/injuries", ttl=1800)
        rows = data.get("data", [])
        if team:
            rows = [r for r in rows if r.get("team") == team]
        return rows

    def team_stats(self, season: int, team: str = "BUF") -> list[dict]:
        data = self.get("/v1/nfl/team-stats", params={"season": season}, ttl=1800)
        return [r for r in data.get("data", []) if r.get("team") == team]

    def player_id(self, name: str, team: str = "BUF") -> str | None:
        roster = self.roster(2026, team)
        q = name.lower().split()
        for r in roster:
            full = r.get("player_name", "").lower()
            if all(part in full for part in q):
                return r.get("player_id")
        return None

    def player_stats(self, player_id: str, season: int) -> list[dict]:
        data = self.get(f"/v1/nfl/players/{player_id}/stats", params={"season": season}, ttl=1800)
        return data.get("data", [])
