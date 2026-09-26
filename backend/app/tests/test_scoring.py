"""Tests for prediction scoring (pure, deterministic)."""

from app.services.scoring import score_predictions


def _actual():
    return {
        "bills_score": 27,
        "opponent_score": 24,
        "first_td_scorer": "Khalil Shakir",
        "allen_passing_yards": 310,
    }


def test_exact_score_and_winner():
    preds = [
        {
            "user_id": 1,
            "bills_score": 27,
            "opponent_score": 24,
            "first_td_scorer": "Khalil Shakir",
            "allen_passing_yards": 310,
        }
    ]
    results = score_predictions(preds, _actual())
    # winner 3 + exact bills 5 + exact opp 5 + first TD 5 + closest total 3 + closest yards 3
    assert results[0]["points"] == 24


def test_wrong_winner_gets_no_winner_points():
    preds = [{"user_id": 1, "bills_score": 10, "opponent_score": 40, "first_td_scorer": "", "allen_passing_yards": 100}]
    results = score_predictions(preds, _actual())
    assert "winner" not in results[0]["breakdown"]


def test_closest_total_awarded_to_one():
    preds = [
        {"user_id": 1, "bills_score": 30, "opponent_score": 20, "first_td_scorer": "", "allen_passing_yards": 200},
        {"user_id": 2, "bills_score": 27, "opponent_score": 24, "first_td_scorer": "", "allen_passing_yards": 310},
        {"user_id": 3, "bills_score": 7, "opponent_score": 3, "first_td_scorer": "", "allen_passing_yards": 500},
    ]
    results = score_predictions(preds, _actual())
    # user 2 total = 51 = actual total -> closest
    assert results[1]["breakdown"]["closest_total"] == 3
    assert "closest_total" not in results[0]["breakdown"]
    assert "closest_total" not in results[2]["breakdown"]


def test_first_td_scorer_case_insensitive():
    preds = [{"user_id": 1, "bills_score": 20, "opponent_score": 10, "first_td_scorer": "khalil shakir", "allen_passing_yards": 100}]
    results = score_predictions(preds, _actual())
    assert results[0]["breakdown"]["first_td_scorer"] == 5
