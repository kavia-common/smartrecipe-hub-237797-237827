from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.config import settings


def _build_database_url() -> str:
    """Build a SQLAlchemy database URL.

    Priority:
    1) If POSTGRES_URL is already a full SQLAlchemy URL, use it.
    2) Otherwise compose from individual POSTGRES_* parts.

    The database container provides a POSTGRES_URL like:
      postgresql://localhost:5000/myapp
    SQLAlchemy + psycopg expects:
      postgresql+psycopg://...
    """
    if settings.POSTGRES_URL:
        url = settings.POSTGRES_URL.strip()
        if url.startswith("postgresql+psycopg://"):
            return url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        # If user provided already (e.g. with +psycopg or other), keep as-is.
        return url

    # Fallback compose (rare in this template)
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    db = settings.POSTGRES_DB
    port = settings.POSTGRES_PORT
    return f"postgresql+psycopg://{user}:{password}@localhost:{port}/{db}"


DATABASE_URL = _build_database_url()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a SQLAlchemy Session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
