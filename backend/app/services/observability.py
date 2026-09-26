"""Observability: record agent runs to the database and (optionally) MLflow.

Recording is best-effort — failures here must never break an agent answer.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from app.db.models import AgentEvidence, AgentRun, AgentToolCall
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def _parse_dt(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass
    return datetime.utcnow()


def record_agent_run(
    question: str,
    mode: str,
    tool_calls: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    llm_latency_ms: int | None,
    total_latency_ms: int | None,
    validation_result: str,
    fallback_used: bool,
) -> int | None:
    try:
        db = SessionLocal()
        run = AgentRun(
            question=question,
            mode=mode,
            llm_latency_ms=llm_latency_ms,
            total_latency_ms=total_latency_ms,
            validation_result=validation_result,
            fallback_used=fallback_used,
        )
        db.add(run)
        db.flush()

        for tc in tool_calls:
            db.add(
                AgentToolCall(
                    run_id=run.id,
                    tool_name=tc["tool"],
                    arguments=str(tc.get("arguments", {})),
                    latency_ms=tc.get("latency_ms"),
                )
            )

        for ev in evidence:
            db.add(
                AgentEvidence(
                    run_id=run.id,
                    source=ev.get("source", ""),
                    tool_name=ev.get("tool", ""),
                    payload=str(ev.get("payload", {})),
                    retrieved_at=_parse_dt(ev.get("retrieved_at")),
                )
            )

        db.commit()
        run_id = run.id
        db.close()
        return run_id
    except Exception as exc:  # pragma: no cover - best effort
        logger.warning("Failed to record agent run: %s", exc)
        return None


def record_mlflow(question: str, mode: str, metrics: dict[str, Any]) -> None:
    """Optionally log to MLflow when MLFLOW_ENABLED=true and mlflow is installed."""
    from app.config import get_settings

    settings = get_settings()
    if not settings.mlflow_enabled:
        return
    try:
        import mlflow

        if settings.mlflow_tracking_uri:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        with mlflow.start_run(run_name="bills_agent"):
            mlflow.log_param("question", question[:200])
            mlflow.log_param("mode", mode)
            mlflow.log_metrics(metrics)
    except ImportError:
        logger.warning("MLFLOW_ENABLED=true but mlflow is not installed.")
    except Exception as exc:  # pragma: no cover
        logger.warning("Failed to log to MLflow: %s", exc)
