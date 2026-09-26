# Architecture

## Data flow

```
Sports data (NFL/sports API)
      ↓
Provider adapter (SportsDataProvider)
      ↓
Normalized data (pydantic models)
      ↓
Agent tools (read-only, return structured JSON + metadata)
      ↓
LLM (tool-calling, reasoning)
      ↓
Grounding validator (claims vs. evidence)
      ↓
API (FastAPI)
      ↓
UI (Next.js)
```

## Layers

### 1. Providers

`backend/app/providers/`

- **Sports** — `SportsDataProvider` interface with `MockSportsProvider` and
  `LiveSportsProvider`. The interface exposes `get_schedule`, `get_game`,
  `get_standings`, `get_roster`, `get_player_stats`, `get_team_stats`,
  `get_play_by_play`, `get_injuries`, `get_historical_games`.
- **News** — `NewsProvider` interface with `MockNewsProvider` and `LiveNewsProvider`.
- **LLM** — provider-agnostic client for OpenAI-compatible APIs, configured via
  `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`.

Provider selection is controlled by `SPORTS_DATA_PROVIDER` / `NEWS_PROVIDER`
(`mock` or `live`). Mock mode is deterministic and requires no credentials.

### 2. Agent

`backend/app/agent/`

- `orchestrator.py` — the agent loop: plan → select tools → execute → gather evidence
  → reason → validate → answer.
- `prompts.py` — system prompts for the four modes (ANALYST, BILLS MAFIA, SIMPLE,
  DEBATE) plus grounding instructions. **Mode changes presentation, never factual
  standards.**
- `tools.py` — tool definitions (JSON schemas) backed by the sports/news providers.
- `grounding.py` — the grounding validator.

### 3. Grounding

LLM output is treated as a **proposal to validate**, not truth. For numerical/factual
claims (scores, records, statistics, standings, dates, times, totals), values must
originate from tool output. The validator:

1. Extracts numerical/factual claims from the draft answer.
2. Checks each claim against stored tool evidence.
3. Rejects unsupported numerical claims.
4. Retries generation once with stronger grounding instructions.
5. Falls back to a deterministic evidence-based answer on repeated failure.

### 4. Database

`backend/app/db/` — SQLAlchemy models + Alembic migrations. Tables:

`games`, `teams`, `players`, `player_stats`, `team_stats`, `standings`,
`news_items`, `agent_runs`, `agent_tool_calls`, `agent_evidence`,
`family_users`, `family_predictions`, `prediction_scores`.

### 5. API

`backend/app/api/` — REST endpoints for schedule, games, standings, roster, stats,
history, news, chat, and family picks. `GET /health` for Railway.

### 6. UI

`frontend/` — Next.js App Router. Pages: Game Day dashboard, Schedule, Stats, Roster,
History, Family Picks, and per-game pages. Chat is the centerpiece with expandable
source citations.

## Agent run flow (observable)

Every run records: `question`, `mode`, selected tools, tool arguments, tool latency,
tool results/evidence IDs, LLM latency, token usage (if available), validation result,
fallback usage, total latency.
