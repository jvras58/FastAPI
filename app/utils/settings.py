"""Settings management for the application using Pydantic."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Class that represents the settings set in the application's .env.
    """

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        secrets_dir='.secrets',
        case_sensitive=True,
        env_ignore_empty=True,
    )

    DB_URL: str
    GROQ_API_KEY: str
    SECURITY_ALGORITHM: str = 'HS256'
    SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SECRETS
    SECURITY_API_SECRET_KEY: str


@lru_cache
def get_settings() -> Settings:
    """Get the application settings, cached for performance."""
    return Settings()  # type: ignore[call-arg]
