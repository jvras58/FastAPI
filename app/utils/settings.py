"""Settings management for the application using Pydantic."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Class that represents the settings set in the application's .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir=".secrets",
        case_sensitive=True,
        env_ignore_empty=True,
    )

    DB_URL: str
    SECURITY_ALGORITHM: str = 'HS256'
    SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SECRETS
    SECURITY_API_SECRET_KEY: str

    # Swagger
    SWAGGER_DOCS_ROUTE: str = '/api/v1/docs'
    SWAGGER_REDOCS_ROUTE: str = '/api/v1/redocs'

    # Configurações de logging e níveis específicos por handler
    LOG_LEVEL: str = 'INFO'

    LOG_FILE: str = 'logs/app.log'
    LOG_MAX_BYTES: int = 10485760
    LOG_BACKUP_COUNT: int = 5
    LOG_CONSOLE_LEVEL: str = 'INFO'
    LOG_FILE_LEVEL: str = 'WARNING'


@lru_cache
def get_settings() -> Settings:
    """Get the application settings, cached for performance."""
    return Settings()
