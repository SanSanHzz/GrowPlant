from os import getenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_client_id: str = getenv("GITHUB_CLIENT_ID", "")
    github_client_secret: str = getenv("GITHUB_CLIENT_SECRET", "")
    github_webhook_secret: str = getenv("GITHUB_WEBHOOK_SECRET", "")
    secret_key: str = getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    database_url: str = getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://growplant:growplant_dev@postgres:5432/growplant",
    )
    redis_url: str = getenv("REDIS_URL", "redis://redis:6379/0")


settings = Settings()
