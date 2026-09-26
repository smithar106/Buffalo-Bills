"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-26

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "teams",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("abbreviation", sa.String(), nullable=False),
        sa.Column("city", sa.String(), default=""),
        sa.Column("conference", sa.String(), default=""),
        sa.Column("division", sa.String(), default=""),
    )
    op.create_table(
        "games",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("season", sa.Integer(), index=True),
        sa.Column("week", sa.Integer()),
        sa.Column("home_team_id", sa.String(), sa.ForeignKey("teams.id")),
        sa.Column("away_team_id", sa.String(), sa.ForeignKey("teams.id")),
        sa.Column("status", sa.String(), default="scheduled"),
        sa.Column("kickoff", sa.DateTime()),
        sa.Column("venue", sa.String(), default=""),
        sa.Column("location", sa.String(), default=""),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
    )
    op.create_table(
        "players",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), index=True),
        sa.Column("number", sa.Integer(), default=0),
        sa.Column("position", sa.String(), default=""),
        sa.Column("team_id", sa.String(), default="buf"),
    )
    op.create_table(
        "standings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("season", sa.Integer(), index=True),
        sa.Column("team_id", sa.String(), sa.ForeignKey("teams.id")),
        sa.Column("wins", sa.Integer(), default=0),
        sa.Column("losses", sa.Integer(), default=0),
        sa.Column("ties", sa.Integer(), default=0),
    )
    op.create_table(
        "team_stats",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("season", sa.Integer(), index=True),
        sa.Column("category", sa.String()),
        sa.Column("value", sa.Float()),
        sa.Column("rank", sa.Integer(), default=0),
    )
    op.create_table(
        "player_stats",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("player_id", sa.String(), sa.ForeignKey("players.id"), index=True),
        sa.Column("season", sa.Integer(), index=True),
        sa.Column("games_played", sa.Integer(), default=0),
        sa.Column("passing_yards", sa.Integer(), default=0),
        sa.Column("passing_tds", sa.Integer(), default=0),
        sa.Column("interceptions", sa.Integer(), default=0),
        sa.Column("rushing_yards", sa.Integer(), default=0),
        sa.Column("rushing_tds", sa.Integer(), default=0),
        sa.Column("receptions", sa.Integer(), default=0),
        sa.Column("receiving_yards", sa.Integer(), default=0),
        sa.Column("receiving_tds", sa.Integer(), default=0),
    )
    op.create_table(
        "news_items",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("title", sa.String()),
        sa.Column("publisher", sa.String(), default=""),
        sa.Column("published_at", sa.DateTime()),
        sa.Column("url", sa.String(), default=""),
        sa.Column("summary", sa.Text(), default=""),
    )
    op.create_table(
        "agent_runs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("question", sa.Text()),
        sa.Column("mode", sa.String(), default="bills_mafia"),
        sa.Column("llm_latency_ms", sa.Integer(), nullable=True),
        sa.Column("total_latency_ms", sa.Integer(), nullable=True),
        sa.Column("validation_result", sa.String(), default="not_validated"),
        sa.Column("fallback_used", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_table(
        "agent_tool_calls",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("agent_runs.id")),
        sa.Column("tool_name", sa.String()),
        sa.Column("arguments", sa.Text(), default="{}"),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
    )
    op.create_table(
        "agent_evidence",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("agent_runs.id")),
        sa.Column("source", sa.String(), default=""),
        sa.Column("tool_name", sa.String(), default=""),
        sa.Column("payload", sa.Text(), default="{}"),
        sa.Column("retrieved_at", sa.DateTime()),
    )
    op.create_table(
        "family_users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), unique=True),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_table(
        "family_predictions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("game_id", sa.String(), index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("family_users.id")),
        sa.Column("bills_score", sa.Integer()),
        sa.Column("opponent_score", sa.Integer()),
        sa.Column("first_td_scorer", sa.String(), default=""),
        sa.Column("allen_passing_yards", sa.Integer(), default=0),
        sa.Column("mvp", sa.String(), default=""),
        sa.Column("locked", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_table(
        "prediction_scores",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("game_id", sa.String(), index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("family_users.id")),
        sa.Column("points", sa.Integer(), default=0),
        sa.Column("breakdown", sa.Text(), default="{}"),
    )


def downgrade() -> None:
    for table in (
        "prediction_scores",
        "family_predictions",
        "family_users",
        "agent_evidence",
        "agent_tool_calls",
        "agent_runs",
        "news_items",
        "player_stats",
        "team_stats",
        "standings",
        "players",
        "games",
        "teams",
    ):
        op.drop_table(table)
