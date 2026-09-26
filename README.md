# BILLS MAFIA AI

> Your family's Buffalo football intelligence agent.

An unofficial, family-focused Buffalo Bills intelligence agent. A tool-using AI that retrieves
current and historical football data through **read-only tools**, reasons over the returned
evidence, and produces **grounded answers with citations** — not a generic chatbot with a
Bills system prompt.

**Core principle:** *The model explains the Bills. The data sources provide the facts.*

---

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js (App Router), TypeScript, Tailwind CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL (SQLAlchemy + Alembic migrations) |
| AI | OpenAI-compatible LLM API, tool-calling agent |
| Deployment | Railway (Dockerfiles) |
| Optional | MLflow (behind `MLFLOW_ENABLED` flag) |

## Repository layout

```
/frontend   Next.js application
/backend    FastAPI application
/docs       Architecture & deployment documentation
/railway    Railway service config + Dockerfiles
```

---

## Local setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 14+ (or Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# database (migrations run from an empty DB)
cp .env.example .env
alembic upgrade head

# run the API (mock mode by default — no external credentials required)
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

---

## Environment variables

See `.env.example` in each service. Key variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_API_KEY` | OpenAI-compatible API key | — |
| `LLM_BASE_URL` | Provider base URL | — |
| `LLM_MODEL` | Model identifier | — |
| `SPORTS_DATA_PROVIDER` | `mock` or `live` | `mock` |
| `BBS_API_KEY` | Big Balls Data key (for `live` sports data) | — |
| `NEWS_PROVIDER` | `mock` or `live` | `mock` |
| `DATABASE_URL` | PostgreSQL connection string | — |
| `MLFLOW_ENABLED` | Enable MLflow tracking | `false` |

The app is fully usable locally in `mock` mode with **no paid API access**.

---

## Development commands

```bash
# backend tests
cd backend && pytest

# frontend build / lint
cd frontend && npm run build && npm run lint

# run golden eval set
cd backend && python scripts/run_evals.py
```

---

## Testing

- Sports provider adapters
- Agent tool schemas
- Grounding validator
- API endpoints
- Prediction scoring
- Data normalization
- Golden agent evaluation set (deterministic mock facts)

---

## Production deployment

See [`docs/RAILWAY_DEPLOYMENT.md`](docs/RAILWAY_DEPLOYMENT.md).

---

## Known limitations

- **Live sports data via Big Balls Data.** `LiveSportsProvider` fetches real NFL
  schedules, scores, standings, rosters, injuries, and player/team stats. It
  requires a `BBS_API_KEY`; play-by-play needs the Pro plan (degrades gracefully).
- **News provider is a stub** — `LiveNewsProvider` needs a news API wired in.
  News stays in mock mode (clearly labeled demo articles).
- **Mock data is a fixed 2026 season** — deterministic and clearly labeled `DEMO DATA`.
- **Family picks use lightweight name-based profiles** (no real authentication) by
  design. Locking at kickoff and automated scoring require a live data source to
  supply the actual result facts (first TD scorer, Allen passing yards).
- **Grounding uses number-presence validation.** It reliably rejects fabricated
  scores/stats, but legitimate derived counts (e.g. "two players injured") can
  occasionally trigger a retry/fallback — which is the intended safe behavior.
- **No rate limiting or auth on the API** — intended for a private family app.
- News is clearly labeled demo content in mock mode; the agent distinguishes
  reported news/analysis from factual sports data.

---

## Disclaimer

**Unofficial fan project. Not affiliated with the Buffalo Bills or NFL.**

