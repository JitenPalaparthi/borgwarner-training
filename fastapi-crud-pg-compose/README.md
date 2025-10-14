# FastAPI CRUD + PostgreSQL (Docker Compose)

Simple CRUD service wired to Postgres using docker-compose.

## Quick Start
```bash
# 1) Start Postgres and the app
docker compose up --build -d

# 2) Open API docs
open http://127.0.0.1:8000/docs
```

## Test with cURL
```bash
# Create
curl -s -X POST http://127.0.0.1:8000/items -H 'Content-Type: application/json'   -d '{"name":"pen","description":"blue ink","price":12.5}' | jq

# List
curl -s http://127.0.0.1:8000/items | jq
```

## Environment
- App reads `DATABASE_URL`. In docker-compose it's set to:
  `postgresql+psycopg2://postgres:postgres@db:5432/appdb`.

## Local Dev without Docker
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# default falls back to SQLite (app.db)
uvicorn app.main:app --reload
```

### To copy date from localmachine to container

```bash
podman cp fastapi-crud-pg-compose ub1:/src
```
