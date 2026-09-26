"""Golden evaluation set for the Bills Mafia AI agent.

Run from the backend directory with the LLM configured:

    python scripts/run_evals.py

Each case asserts deterministic mock-data facts. Results are printed as a
pass/fail report; the process exits non-zero if any case fails.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent import run

# (question, expected_tool, expected_facts, expect_no_fallback)
CASES = [
    ("Who do the Bills play next?", "get_next_game", ["chargers"], True),
    ("What is Buffalo's record?", "get_standings", ["3", "0"], True),
    ("Who leads the Bills in receiving?", "get_player_stats", ["khalil shakir", "280"], True),
    ("How many passing yards did Josh Allen have?", "get_player_stats", ["835"], True),
    ("How have the Bills done against Miami?", "get_head_to_head", ["3"], True),
]


def main() -> int:
    results = []
    for question, expected_tool, facts, no_fallback in CASES:
        r = run(question, "analyst")
        answer = r["answer"].lower()
        tools = [t["tool"] for t in r["tool_calls"]]

        checks = {
            "tool_selection": expected_tool in tools,
            "grounded (no fallback)": (not r["fallback"]) if no_fallback else True,
            "has_citations": len(r["sources"]) >= 1,
            "facts_present": all(f.lower() in answer for f in facts),
        }
        passed = all(checks.values())
        results.append((question, checks, tools, r["validation"]["result"]))

    print("=" * 70)
    print("BILLS MAFIA AI — GOLDEN EVAL REPORT")
    print("=" * 70)
    for question, checks, tools, validation in results:
        status = "PASS" if all(checks.values()) else "FAIL"
        print(f"\n[{status}] {question}")
        print(f"  tools used: {tools}")
        print(f"  validation: {validation}")
        for name, ok in checks.items():
            print(f"    {'ok' if ok else 'MISS'}  {name}")

    total = len(results)
    passed = sum(1 for _, c, _, _ in results if all(c.values()))
    print("\n" + "=" * 70)
    print(f"RESULT: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
