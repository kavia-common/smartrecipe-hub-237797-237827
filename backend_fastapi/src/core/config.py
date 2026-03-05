from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Note: Do not hardcode secrets; request the orchestrator to set env vars in .env.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    #
    # The generated template primarily uses POSTGRES_* variables provided by the
    # database container. Some deployments (and this bug report) provide a single
    # DATABASE_URL instead. We support both.
    #
    # If DATABASE_URL is set, it may be e.g.:
    #   postgresql://user:pass@host:port/dbname
    # or SQLAlchemy form:
    #   postgresql+psycopg://user:pass@host:port/dbname
    POSTGRES_URL: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_PORT: str = ""
    DATABASE_URL: str = ""

    # Auth
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    #
    # Historically this template used CORS_ALLOW_ORIGINS. Some environments use
    # CORS_ORIGINS or ALLOWED_ORIGINS instead. We support all three; the app will
    # pick the first non-empty value.
    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ORIGINS: str = ""
    ALLOWED_ORIGINS: str = ""


settings = Settings()
