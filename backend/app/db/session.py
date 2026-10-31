import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

_database_url = settings.database_url
# Resolve relative sqlite paths against the backend directory so the app works
# regardless of the current working directory it is launched from.
if _database_url.startswith("sqlite:///"):
    rel_path = _database_url[len("sqlite:///"):]
    if not os.path.isabs(rel_path):
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        abs_path = os.path.join(backend_dir, rel_path)
        _database_url = "sqlite:///" + abs_path

engine = create_engine(
    _database_url,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. For production, use Alembic migrations instead."""
    Base.metadata.create_all(bind=engine)
