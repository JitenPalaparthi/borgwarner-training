# alembic/env.py
import os
from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

config = context.config

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://appuser:apppass@db:5432/appdb")
SYNC_URL = DATABASE_URL.replace("+asyncpg", "")  # Alembic needs sync

target_metadata = None

def run_migrations_offline():
    context.configure(
        url=SYNC_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Only pass SQLAlchemy-* names by using a prefix and a tiny dict
    engine = engine_from_config(
        {"sqlalchemy.url": SYNC_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()