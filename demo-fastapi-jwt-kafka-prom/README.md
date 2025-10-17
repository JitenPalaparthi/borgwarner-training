# FastAPI + JWT + Postgres + Kafka + Prometheus + Grafana + Alembic (Demo)

## Run
```bash
cp .env.example .env
docker compose up --build -d
# API Docs:   http://localhost:8000/docs
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000  (admin / admin)
```
Alembic migrations run automatically at container start (`entrypoint.sh`).  
Kafka topic auto-create is enabled at the broker and also attempted by the app via admin client.

## APIs
- `POST /register`
- `POST /login` -> JWT
- `GET /me` (protected)
- `POST /produce` (protected) -> produces to Kafka
- `GET /messages` (protected) -> reads consumed messages persisted to Postgres

## Grafana
Provisioned Prometheus datasource and a starter dashboard at **General → FastAPI Demo Observability**.
