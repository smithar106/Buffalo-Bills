# Railway Deployment

## Services

| Service | Type | Notes |
|---------|------|-------|
| `bills-web` | Next.js | Frontend, proxies `/api` to `bills-api` |
| `bills-api` | FastAPI | Backend API + agent |
| `PostgreSQL` | Database | Railway-provided |
| `MLflow` | optional | Only if `MLFLOW_ENABLED=true` |

## Configuration

Railway uses the `Dockerfile` in each service directory. Set environment
variables per-service in the Railway dashboard (never commit secrets).

### bills-web

- `NEXT_PUBLIC_API_URL` — public URL of `bills-api` (e.g. the Railway-provided URL)
- `PORT` — Railway injects this; Next.js should respect it

### bills-api

- `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`
- `SPORTS_DATA_PROVIDER` (`mock` or `live`)
- `NEWS_PROVIDER` (`mock` or `live`)
- `DATABASE_URL` — Railway PostgreSQL connection string
- `MLFLOW_ENABLED` (`true`/`false`)
- `CORS_ORIGINS` — comma-separated allowed origins

## Health checks

- Backend: `GET /health` → `{"status": "ok"}`. Configure Railway healthcheck to
  this path for `bills-api`.
- Frontend: serves `/api/health` locally; Railway healthcheck can hit `/`.

## Migrations

Run `alembic upgrade head` on deploy. In Railway this runs as part of the
`bills-api` start command (see the API Dockerfile/start script).

## CORS

The backend reads `CORS_ORIGINS` and restricts origins accordingly. In
production, restrict to the deployed frontend domain.

## Production error handling

- The API returns structured JSON errors and never leaks stack traces.
- The agent handles LLM/sports-provider failure with deterministic fallbacks.
