"""Tests for the family predictions API (isolated SQLite DB)."""

import tempfile

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base
from app.db.session import get_db
from app.main import app

tmp = tempfile.NamedTemporaryFile(suffix=".db")
engine = create_engine(f"sqlite:///{tmp.name}", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_db
client = TestClient(app)


def test_create_user_and_leaderboard_flow():
    r = client.post("/api/family/users", json={"name": "Grandpa"})
    assert r.status_code == 200
    user_id = r.json()["user"]["id"]

    r = client.get("/api/family/leaderboard")
    assert r.status_code == 200
    rows = r.json()["leaderboard"]
    assert any(row["name"] == "Grandpa" for row in rows)


def test_submit_prediction():
    r = client.post("/api/family/users", json={"name": "Aunt Sue"})
    user_id = r.json()["user"]["id"]

    r = client.post(
        "/api/family/predictions",
        json={
            "user_id": user_id,
            "bills_score": 31,
            "opponent_score": 28,
            "first_td_scorer": "Josh Allen",
            "allen_passing_yards": 300,
            "mvp": "Josh Allen",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["prediction"]["bills_score"] == 31
    assert data["game"]["id"].startswith("2026")


def test_score_game_404_unknown():
    r = client.post("/api/family/score?game_id=does-not-exist")
    assert r.status_code == 404


def test_full_score_flow_updates_leaderboard():
    r = client.post("/api/family/users", json={"name": "Uncle Joe"})
    user_id = r.json()["user"]["id"]

    # Insert a prediction for a completed game directly (normally locked at kickoff).
    db = TestingSession()
    from app.db.models import FamilyPrediction

    db.add(
        FamilyPrediction(
            game_id="2026-w1-buf-nyj",
            user_id=user_id,
            bills_score=34,
            opponent_score=17,
            first_td_scorer="Josh Allen",
            allen_passing_yards=285,
        )
    )
    db.commit()
    db.close()

    r = client.post("/api/family/score?game_id=2026-w1-buf-nyj")
    assert r.status_code == 200
    assert r.json()["scored"] == 1
    # Perfect pick: winner 3 + exact bills 5 + exact opp 5 + first TD 5 + closest total 3 + closest yards 3 = 24
    assert r.json()["results"][0]["points"] == 24

    r = client.get("/api/family/leaderboard")
    uncle = [row for row in r.json()["leaderboard"] if row["name"] == "Uncle Joe"][0]
    assert uncle["season_points"] == 24
    assert uncle["correct_picks"] == 1
