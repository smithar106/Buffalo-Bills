"""Normalized sports data models shared across providers and tools."""

from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


class Team(BaseModel):
    id: str
    name: str
    abbreviation: str
    city: str
    conference: str
    division: str


class QuarterScore(BaseModel):
    quarter: int
    home: int
    away: int


class Game(BaseModel):
    id: str
    season: int
    week: int
    home_team: Team
    away_team: Team
    status: Literal["scheduled", "live", "final"]
    kickoff: datetime
    venue: str
    location: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    quarter_scores: list[QuarterScore] = Field(default_factory=list)
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StandingsEntry(BaseModel):
    team: Team
    wins: int
    losses: int
    ties: int
    win_pct: float
    division_wins: int
    division_losses: int
    points_for: int
    points_against: int
    season: int
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Player(BaseModel):
    id: str
    name: str
    number: int
    position: str
    height: str
    weight: int
    college: str
    experience: int
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PlayerSeasonStat(BaseModel):
    player: Player
    season: int
    games_played: int
    # Offense
    passing_yards: int = 0
    passing_tds: int = 0
    interceptions: int = 0
    rushing_yards: int = 0
    rushing_tds: int = 0
    receptions: int = 0
    receiving_yards: int = 0
    receiving_tds: int = 0
    # Defense
    tackles: int = 0
    sacks: float = 0.0
    # Special teams
    field_goals_made: int = 0
    field_goals_attempted: int = 0
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PlayerGameLogEntry(BaseModel):
    game_id: str
    season: int
    week: int
    opponent: str
    passing_yards: int = 0
    passing_tds: int = 0
    interceptions: int = 0
    rushing_yards: int = 0
    rushing_tds: int = 0
    receptions: int = 0
    receiving_yards: int = 0
    receiving_tds: int = 0
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TeamStat(BaseModel):
    season: int
    category: str
    value: float
    rank: int
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Play(BaseModel):
    game_id: str
    play_id: str
    quarter: int
    time: str
    down: int
    yards_to_go: int
    description: str
    offense: str
    points: int = 0
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Injury(BaseModel):
    player: Player
    status: str
    injury: str
    updated: datetime
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HeadToHead(BaseModel):
    team_a: Team
    team_b: Team
    start_season: int
    end_season: int
    meetings: list[Game]
    team_a_wins: int
    team_b_wins: int
    source: str = "mock"
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
