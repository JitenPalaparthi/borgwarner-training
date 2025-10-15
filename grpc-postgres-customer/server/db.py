import os
import asyncpg
from typing import Optional, Dict, Any

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/app")

_pool: Optional[asyncpg.pool.Pool] = None

async def init_pool() -> None:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn=DATABASE_URL, min_size=1, max_size=10)

async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None

async def fetchrow(query: str, *args):
    assert _pool is not None
    return await _pool.fetchrow(query, *args)

async def fetch(query: str, *args):
    assert _pool is not None
    return await _pool.fetch(query, *args)

async def execute(query: str, *args) -> str:
    assert _pool is not None
    return await _pool.execute(query, *args)

def record_to_customer(rec: asyncpg.Record):
    created_at = rec["created_at"]
    created_at_unix = int(created_at.timestamp()) if created_at else 0
    return {
        "id": rec["id"],
        "name": rec["name"],
        "email": rec["email"],
        "phone": rec["phone"] or "",
        "created_at_unix": created_at_unix,
    }
