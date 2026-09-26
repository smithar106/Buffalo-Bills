"""Grounding validator.

Treats LLM output as a proposal to validate. Extracts numerical claims from an
answer and verifies each appears in the tool evidence. Unsupported numbers cause
rejection + retry; repeated failure triggers a deterministic fallback.
"""

from __future__ import annotations

import json
import re
from typing import Any

NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


def _norm(num: str) -> float | None:
    try:
        return float(num)
    except ValueError:
        return None


def _extract_numbers(text: str) -> list[str]:
    return NUMBER_RE.findall(text)


def _evidence_number_strings(evidence: list[dict[str, Any]]) -> set[str]:
    """Collect every number token present anywhere in the evidence payloads."""
    raw = json.dumps([e.get("payload", {}) for e in evidence], default=str)
    return set(NUMBER_RE.findall(raw))


def validate_answer(answer: str, evidence: list[dict[str, Any]]) -> list[str]:
    """Return the list of numbers in `answer` not supported by `evidence`."""
    if not evidence:
        # With no tool evidence, any number is unsupported.
        return _extract_numbers(answer)

    ev_raw = _evidence_number_strings(evidence)
    ev_float = {_norm(n) for n in ev_raw}
    ev_float.discard(None)

    unsupported: list[str] = []
    for num in _extract_numbers(answer):
        if num in ev_raw:
            continue
        f = _norm(num)
        if f is not None and f in ev_float:
            continue
        unsupported.append(num)
    return unsupported


def build_fallback_answer(evidence: list[dict[str, Any]]) -> str:
    """Deterministic evidence-based fallback when grounding repeatedly fails."""
    if not evidence:
        return "I couldn't verify that from the available Bills data."

    lines = ["I couldn't fully verify an answer, so here is the raw data I retrieved:"]
    for e in evidence:
        src = e.get("source", e.get("tool"))
        lines.append(f"\n[{src}]")
        lines.append(json.dumps(e.get("payload", {}), default=str, ensure_ascii=False))
    return "\n".join(lines)
