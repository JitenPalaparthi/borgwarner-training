#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for Postgres at ${DATABASE_URL}..."

# retry loop (max ~60s)
for i in $(seq 1 60); do
python - <<'PY' && break || true
import os,asyncio,sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine
url = os.environ.get("DATABASE_URL","postgresql+asyncpg://appuser:apppass@db:5432/appdb")
async def check():
    engine = create_async_engine(url)
    try:
        async with engine.connect() as conn:
            await conn.execute(sa.text("SELECT 1"))
    finally:
        await engine.dispose()
asyncio.run(check())
print("DB reachable")
PY
echo "DB not ready yet, retrying ($i/60)..."
sleep 1
done

# Run migrations
alembic upgrade head

# Start API
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
