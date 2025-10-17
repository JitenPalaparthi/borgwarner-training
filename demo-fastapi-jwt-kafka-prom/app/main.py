import asyncio, logging
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
try:
    from prometheus_fastapi_instrumentator import Instrumentator
    _HAS_METRICS = True
except ImportError:
    _HAS_METRICS = False

from sqlalchemy import select, desc
from .database import SessionLocal
from .models import User, Message
from .schemas import RegisterIn, LoginIn, TokenOut, ProduceIn, MessageOut
from .auth import hash_password, verify_password, create_access_token
from .deps import get_current_user
from .kafka_worker import send_message, consumer_loop, ensure_topic

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Demo FastAPI JWT + Postgres + Kafka (official) + Prometheus + Grafana + Alembic")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if _HAS_METRICS:
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")

stop_event = asyncio.Event()
consumer_task: asyncio.Task | None = None

@app.on_event("startup")
async def on_startup():
    # Wait for Kafka with retries, then start consumer
    await ensure_topic()
    global consumer_task
    consumer_task = asyncio.create_task(consumer_loop(stop_event))
    logger.info("Startup complete")

@app.on_event("shutdown")
async def on_shutdown():
    stop_event.set()
    if consumer_task:
        await consumer_task

@app.post("/register", response_model=dict)
async def register(payload: RegisterIn):
    async with SessionLocal() as session:
        existing = (await session.execute(select(User).where(User.email == payload.email))).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user = User(email=payload.email, password_hash=hash_password(payload.password))
        session.add(user)
        await session.commit()
        return {"ok": True}

@app.post("/login", response_model=TokenOut)
async def login(payload: LoginIn):
    async with SessionLocal() as session:
        user = (await session.execute(select(User).where(User.email == payload.email))).scalar_one_or_none()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = create_access_token(str(user.id))
        return TokenOut(access_token=token)

@app.get("/me", response_model=dict)
async def me(user_id: str = Depends(get_current_user)):
    async with SessionLocal() as session:
        user = (await session.execute(select(User).where(User.id == int(user_id)))).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": user.id, "email": user.email}

@app.post("/produce", response_model=dict)
async def produce(data: ProduceIn, user_id: str = Depends(get_current_user)):
    await send_message(text=data.text, key=user_id)
    return {"queued": True}

@app.get("/messages", response_model=List[MessageOut])
async def list_messages(user_id: str = Depends(get_current_user)):
    async with SessionLocal() as session:
        res = await session.execute(select(Message).order_by(desc(Message.id)).limit(50))
        rows = res.scalars().all()
        return [MessageOut(id=m.id, text=m.text) for m in rows]
