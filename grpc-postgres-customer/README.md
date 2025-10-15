# grpc-postgres-customer (fully containerized server + Postgres)

This is a minimal async **gRPC** service in Python (`grpc.aio`) that talks to **PostgreSQL** via **asyncpg**.

## Prereqs
- Docker + Docker Compose v2

## Quickstart
```bash
# In project root
docker compose up -d --build

# Test the service from your host (needs Python to run the sample client)
python -m venv venv && source venv/bin/activate
pip install grpcio
python client/client.py
```

## Proto
See `proto/customer.proto`.

## Notes
- Service listens on `:50051` (mapped to host).
- DB runs on Postgres 16; the database `app` is created with a `customers` table via `migrations/init.sql`.
- Server builds a Docker image that runs `python -m server.app`. During the image build, gRPC stubs are generated into `server/`.

## Environment
- `DATABASE_URL` (default: `postgresql://postgres:postgres@db:5432/app`)
- `PORT` (default: `50051`)

## Regenerating stubs locally (optional)
```bash
pip install grpcio-tools
python -m grpc_tools.protoc -I proto       --python_out=server --grpc_python_out=server proto/customer.proto
```
