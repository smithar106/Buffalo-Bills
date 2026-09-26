"""Family prediction scoring.

Pure, deterministic functions — no I/O, no LLM. Calculated by code, not the model.

Scoring rules:
  - Correct winner            = 3
  - Exact Bills score         = 5
  - Exact opponent score      = 5
  - Closest total score       = 3 (group-level)
  - Correct first TD scorer   = 5
  - Closest Josh passing yds  = 3 (group-level)
"""

from __future__ import annotations

from typing import Any


def _winner_points(pred_bills: int, pred_opp: int, act_bills: int, act_opp: int) -> int:
    pred_win = pred_bills > pred_opp
    act_win = act_bills > act_opp
    if pred_bills == pred_opp or act_bills == act_opp:
        return 0
    return 3 if pred_win == act_win else 0


def score_predictions(predictions: list[dict[str, Any]], actual: dict[str, Any]) -> list[dict[str, Any]]:
    """Score a group of predictions against one actual game result.

    Group-level awards (closest total, closest yards) are computed across all
    predictions for the same game.
    """
    act_bills = int(actual["bills_score"])
    act_opp = int(actual["opponent_score"])
    act_total = act_bills + act_opp
    act_scorer = (actual.get("first_td_scorer") or "").strip().lower()
    act_yards = int(actual.get("allen_passing_yards") or 0)

    total_diffs = [
        abs(int(p["bills_score"]) + int(p["opponent_score"]) - act_total)
        for p in predictions
    ]
    min_total_diff = min(total_diffs) if total_diffs else None

    yard_diffs = [
        abs(int(p.get("allen_passing_yards") or 0) - act_yards)
        for p in predictions
    ]
    min_yard_diff = min(yard_diffs) if yard_diffs else None

    results: list[dict[str, Any]] = []
    for idx, p in enumerate(predictions):
        points = 0
        breakdown: dict[str, int] = {}

        w = _winner_points(int(p["bills_score"]), int(p["opponent_score"]), act_bills, act_opp)
        if w:
            points += w
            breakdown["winner"] = w

        if int(p["bills_score"]) == act_bills:
            points += 5
            breakdown["exact_bills_score"] = 5
        if int(p["opponent_score"]) == act_opp:
            points += 5
            breakdown["exact_opponent_score"] = 5

        scorer = (p.get("first_td_scorer") or "").strip().lower()
        if scorer and scorer == act_scorer:
            points += 5
            breakdown["first_td_scorer"] = 5

        if min_total_diff is not None and total_diffs[idx] == min_total_diff:
            points += 3
            breakdown["closest_total"] = 3

        if min_yard_diff is not None and yard_diffs[idx] == min_yard_diff:
            points += 3
            breakdown["closest_allen_yards"] = 3

        results.append(
            {
                "user_id": p["user_id"],
                "points": points,
                "breakdown": breakdown,
            }
        )

    return results
