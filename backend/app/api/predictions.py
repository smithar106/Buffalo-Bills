"""Family predictions API.

Lightweight: no authentication in the demo (profiles are keyed by name). In
production the endpoints would sit behind a family-level gate.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import FamilyPrediction, FamilyUser, PredictionScore
from app.db.session import get_db
from app.providers.sports import get_sports_provider
from app.services.scoring import score_predictions

router = APIRouter(prefix="/api/family", tags=["family"])


class CreateUserRequest(BaseModel):
    name: str


class CreatePredictionRequest(BaseModel):
    user_id: int
    bills_score: int
    opponent_score: int
    first_td_scorer: str = ""
    allen_passing_yards: int = 0
    mvp: str = ""


@router.post("/users")
def create_user(req: CreateUserRequest, db: Session = Depends(get_db)):
    name = req.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    existing = db.query(FamilyUser).filter(FamilyUser.name == name).first()
    if existing:
        return {"user": {"id": existing.id, "name": existing.name}}
    user = FamilyUser(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user": {"id": user.id, "name": user.name}}


@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(FamilyUser).order_by(FamilyUser.name).all()
    return {"users": [{"id": u.id, "name": u.name} for u in users]}


@router.post("/predictions")
def create_prediction(req: CreatePredictionRequest, db: Session = Depends(get_db)):
    user = db.get(FamilyUser, req.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    provider = get_sports_provider()
    game = provider.get_next_game()
    existing = (
        db.query(FamilyPrediction)
        .filter(FamilyPrediction.game_id == game.id, FamilyPrediction.user_id == req.user_id)
        .first()
    )

    pred = existing or FamilyPrediction(game_id=game.id, user_id=req.user_id)
    pred.bills_score = req.bills_score
    pred.opponent_score = req.opponent_score
    pred.first_td_scorer = req.first_td_scorer
    pred.allen_passing_yards = req.allen_passing_yards
    pred.mvp = req.mvp
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return {
        "prediction": {
            "id": pred.id,
            "game_id": pred.game_id,
            "user_id": pred.user_id,
            "bills_score": pred.bills_score,
            "opponent_score": pred.opponent_score,
            "first_td_scorer": pred.first_td_scorer,
            "allen_passing_yards": pred.allen_passing_yards,
            "mvp": pred.mvp,
        },
        "game": {
            "id": game.id,
            "opponent": game.away_team.abbreviation if game.home_team.id == "buf" else game.home_team.abbreviation,
            "kickoff": game.kickoff.isoformat(),
        },
    }


@router.post("/score")
def score_game(game_id: str, db: Session = Depends(get_db)):
    provider = get_sports_provider()
    actual = provider.get_game_actual(game_id)
    if actual is None:
        raise HTTPException(status_code=404, detail="No result available for this game")

    preds = db.query(FamilyPrediction).filter(FamilyPrediction.game_id == game_id).all()
    if not preds:
        return {"scored": 0, "results": []}

    rows = [
        {
            "user_id": p.user_id,
            "bills_score": p.bills_score,
            "opponent_score": p.opponent_score,
            "first_td_scorer": p.first_td_scorer,
            "allen_passing_yards": p.allen_passing_yards,
        }
        for p in preds
    ]
    results = score_predictions(rows, actual)

    for r in results:
        existing = (
            db.query(PredictionScore)
            .filter(PredictionScore.game_id == game_id, PredictionScore.user_id == r["user_id"])
            .first()
        )
        row = existing or PredictionScore(game_id=game_id, user_id=r["user_id"])
        row.points = r["points"]
        row.breakdown = str(r["breakdown"])
        db.add(row)
    db.commit()

    return {"scored": len(results), "results": results, "actual": actual}


@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    users = db.query(FamilyUser).all()
    rows = []
    for u in users:
        scores = db.query(PredictionScore).filter(PredictionScore.user_id == u.id).all()
        season_points = sum(s.points for s in scores)
        weekly_points = scores[-1].points if scores else 0
        # "correct picks" = number of scored predictions that earned >= 3 points.
        correct = sum(1 for s in scores if s.points >= 3)
        rows.append(
            {
                "name": u.name,
                "weekly_points": weekly_points,
                "season_points": season_points,
                "correct_picks": correct,
            }
        )
    rows.sort(key=lambda r: (-r["season_points"], -r["weekly_points"], r["name"]))
    return {"leaderboard": rows}
