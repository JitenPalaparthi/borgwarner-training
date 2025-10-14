# Python FastAPI File Upload + Docker

Minimal FastAPI service for file uploads, with Dockerfile and docker-compose.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

## Docker
```bash
docker build -t py-file-upload:latest .
mkdir -p uploads
docker run --rm -p 8000:8000 -v $(pwd)/uploads:/uploads -e UPLOAD_DIR=/uploads py-file-upload:latest
```

## docker-compose
```bash
mkdir -p uploads
docker compose up --build -d
# open http://127.0.0.1:8000/docs
```

### Endpoints
- POST /upload — single file
- POST /upload/many — multiple files
- POST /upload/images — only JPEG/PNG

Uploaded files persist to ./uploads on host (mapped to /uploads in the container).
