from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os, shutil

app = FastAPI(title="Python File Upload API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}

@app.post("/upload", tags=["upload"])
async def upload(file: UploadFile = File(...)):
    dest = os.path.join(UPLOAD_DIR, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename, "content_type": file.content_type, "saved_to": dest}

@app.post("/upload/many", tags=["upload"])
async def upload_many(files: List[UploadFile] = File(...)):
    saved = []
    for file in files:
        dest = os.path.join(UPLOAD_DIR, file.filename)
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved.append({"filename": file.filename, "saved_to": dest})
    return {"count": len(saved), "files": saved}

@app.post("/upload/images", tags=["upload"])
async def upload_images(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only JPEG/PNG allowed")
    dest = os.path.join(UPLOAD_DIR, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "ok", "saved_to": dest}
