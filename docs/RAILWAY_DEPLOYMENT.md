# Railway Deployment

## Services

| Service | Directory | Health check | Notes |
|---------|-----------|--------------|-------|
| `bills-web` | `frontend/` | `/healthz` | Next.js (standalone), proxies `/api/*` → `bills-api` via middleware |
| `bills-api` | `backend/` | `/health` | FastAPI, runs `alembic upgrade head` on start |
| `PostgreSQL` | Railway-managed | — | Inject connection string via `DATABASE_URL` |
| `MLflow` | optional | — | Only if `MLFLOW_ENABLED=true` |

Each service has its own `Dockerfile` and `railway.json`.

## Setup

1. Create a new Railway project and add three services from this repo
   (each pointed at its subdirectory: `frontend`, `backend`, and a PostgreSQL plugin).
2. Set the environment variables below per service.
3. Deploy. `bills-api` runs migrations automatically on start.

## Environment variables

### bills-api (`backend/`)

| Variable | Description |
|----------|-------------|
| `LLM_API_KEY` | OpenAI-compatible API key |
| `LLM_BASE_URL` | Provider base URL (default `https://api.openai.com/v1`) |
| `LLM_MODEL` | Model id (e.g. `gpt-4o-mini`) |
| `SPORTS_DATA_PROVIDER` | `mock` or `live` |
| `NEWS_PROVIDER` | `mock` or `live` |
| `DATABASE_URL` | Railway PostgreSQL connection string (auto-injected) |
| `CORS_ORIGINS` | Comma-separated frontend origins |
| `MLFLOW_ENABLED` | `true`/`false` |
| `MLFLOW_TRACKING_URI` | MLflow tracking server URI (optional) |

### bills-web (`frontend/`)

| Variable | Description |
|----------|-------------|
| `API_URL` | URL of the `bills-api` service. Use the private network address `http://bills-api.railway.internal:8080` (recommended) or a public domain. |

> The `/api/*` proxy is implemented in `frontend/middleware.ts` (runtime), so
> `API_URL` is read at request time — not baked into the build.

## CORS

`CORS_ORIGINS` on the API must include the deployed `bills-web` origin (e.g.
`https://bills-web-production-XXXX.up.railway.app`). Client-side requests go
through the same-origin `/api` rewrite, but the API also allows direct calls
from the frontend if needed.

## Health checks

- `bills-api`: `GET /health` → `{"status": "ok"}`.
- `bills-web`: `GET /healthz` → `{"status": "ok"}`.

## Migrations

`bills-api` runs `alembic upgrade head` on every start (see `backend/start.sh`),
so schema changes apply automatically from an empty or existing database.

## Secrets

Never commit secrets. All credentials are injected via Railway environment
variables; `.env` files are gitignored.
