"""API endpoint tests."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_next_game():
    resp = client.get("/api/next-game")
    assert resp.status_code == 200
    data = resp.json()
    assert data["game"]["status"] == "scheduled"
    assert data["demo"] is True


def test_standings():
    resp = client.get("/api/standings")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["standings"]) == 4


def test_game_404():
    resp = client.get("/api/games/does-not-exist")
    assert resp.status_code == 404


def test_news():
    resp = client.get("/api/news")
    assert resp.status_code == 200
    assert len(resp.json()["news"]) >= 1
