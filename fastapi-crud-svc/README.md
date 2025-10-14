
# FastAPI CRUD Service (Items)

Simple CRUD for `Item` with FastAPI + SQLAlchemy (SQLite by default).

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open docs: http://127.0.0.1:8000/docs

## Quick cURL
```bash
# Create
curl -s -X POST http://127.0.0.1:8000/items -H 'Content-Type: application/json'   -d '{"name":"pen","description":"blue ink","price":12.5}' | jq

# List
curl -s http://127.0.0.1:8000/items | jq

# Get
curl -s http://127.0.0.1:8000/items/1 | jq

# Patch
curl -s -X PATCH http://127.0.0.1:8000/items/1 -H 'Content-Type: application/json'   -d '{"price": 9.99}' | jq

# Delete
curl -i -X DELETE http://127.0.0.1:8000/items/1
```

## Docker
```bash
docker build -t fastapi-crud:latest .
docker run --rm -p 8000:8000 fastapi-crud:latest
```
