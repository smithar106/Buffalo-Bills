"""SQLAlchemy models for persistence."""

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    abbreviation: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, default="")
    conference: Mapped[str] = mapped_column(String, default="")
    division: Mapped[str] = mapped_column(String, default="")


class Game(Base):
    __tablename__ = "games"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    season: Mapped[int] = mapped_column(Integer, index=True)
    week: Mapped[int] = mapped_column(Integer)
    home_team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"))
    away_team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"))
    status: Mapped[str] = mapped_column(String, default="scheduled")
    kickoff: Mapped[datetime] = mapped_column(DateTime)
    venue: Mapped[str] = mapped_column(String, default="")
    location: Mapped[str] = mapped_column(String, default="")
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Player(Base):
    __tablename__ = "players"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    number: Mapped[int] = mapped_column(Integer, default=0)
    position: Mapped[str] = mapped_column(String, default="")
    team_id: Mapped[str] = mapped_column(String, default="buf")


class Standings(Base):
    __tablename__ = "standings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season: Mapped[int] = mapped_column(Integer, index=True)
    team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"))
    wins: Mapped[int] = mapped_column(Integer, default=0)
    losses: Mapped[int] = mapped_column(Integer, default=0)
    ties: Mapped[int] = mapped_column(Integer, default=0)


class TeamStat(Base):
    __tablename__ = "team_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season: Mapped[int] = mapped_column(Integer, index=True)
    category: Mapped[str] = mapped_column(String)
    value: Mapped[float] = mapped_column(Float)
    rank: Mapped[int] = mapped_column(Integer, default=0)


class PlayerStat(Base):
    __tablename__ = "player_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[str] = mapped_column(String, ForeignKey("players.id"), index=True)
    season: Mapped[int] = mapped_column(Integer, index=True)
    games_played: Mapped[int] = mapped_column(Integer, default=0)
    passing_yards: Mapped[int] = mapped_column(Integer, default=0)
    passing_tds: Mapped[int] = mapped_column(Integer, default=0)
    interceptions: Mapped[int] = mapped_column(Integer, default=0)
    rushing_yards: Mapped[int] = mapped_column(Integer, default=0)
    rushing_tds: Mapped[int] = mapped_column(Integer, default=0)
    receptions: Mapped[int] = mapped_column(Integer, default=0)
    receiving_yards: Mapped[int] = mapped_column(Integer, default=0)
    receiving_tds: Mapped[int] = mapped_column(Integer, default=0)


class NewsItem(Base):
    __tablename__ = "news_items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    publisher: Mapped[str] = mapped_column(String, default="")
    published_at: Mapped[datetime] = mapped_column(DateTime)
    url: Mapped[str] = mapped_column(String, default="")
    summary: Mapped[str] = mapped_column(Text, default="")


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text)
    mode: Mapped[str] = mapped_column(String, default="bills_mafia")
    llm_latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    validation_result: Mapped[str] = mapped_column(String, default="not_validated")
    fallback_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class AgentToolCall(Base):
    __tablename__ = "agent_tool_calls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(Integer, ForeignKey("agent_runs.id"))
    tool_name: Mapped[str] = mapped_column(String)
    arguments: Mapped[str] = mapped_column(Text, default="{}")
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)


class AgentEvidence(Base):
    __tablename__ = "agent_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(Integer, ForeignKey("agent_runs.id"))
    source: Mapped[str] = mapped_column(String, default="")
    tool_name: Mapped[str] = mapped_column(String, default="")
    payload: Mapped[str] = mapped_column(Text, default="{}")
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class FamilyUser(Base):
    __tablename__ = "family_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class FamilyPrediction(Base):
    __tablename__ = "family_predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(String, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("family_users.id"))
    bills_score: Mapped[int] = mapped_column(Integer)
    opponent_score: Mapped[int] = mapped_column(Integer)
    first_td_scorer: Mapped[str] = mapped_column(String, default="")
    allen_passing_yards: Mapped[int] = mapped_column(Integer, default=0)
    mvp: Mapped[str] = mapped_column(String, default="")
    locked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class PredictionScore(Base):
    __tablename__ = "prediction_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(String, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("family_users.id"))
    points: Mapped[int] = mapped_column(Integer, default=0)
    breakdown: Mapped[str] = mapped_column(Text, default="{}")
