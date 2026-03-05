from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.config import settings


def _build_database_url() -> str:
    """Build a SQLAlchemy database URL.

    Priority:
    1) DATABASE_URL (single env var) if set.
    2) POSTGRES_URL if set.
    3) Compose from individual POSTGRES_* parts.

    Notes:
    - Some environments provide `DATABASE_URL=postgresql://...`
    - SQLAlchemy + psycopg expects `postgresql+psycopg://...`
    """

    def _normalize(url: str) -> str:
        url = url.strip()
        if url.startswith("postgresql+psycopg://"):
            return url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    if settings.DATABASE_URL:
        return _normalize(settings.DATABASE_URL)

    if settings.POSTGRES_URL:
        return _normalize(settings.POSTGRES_URL)

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
