from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Note: Do not hardcode secrets; request the orchestrator to set env vars in .env.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database (names must match running_containers.database_postgresql.db_env_vars)
    POSTGRES_URL: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_PORT: str = ""

    # Auth
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ALLOW_ORIGINS: str = "*"


settings = Settings()
