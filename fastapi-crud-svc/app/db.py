
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# SQLite file DB (change to Postgres by replacing DATABASE_URL)
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
