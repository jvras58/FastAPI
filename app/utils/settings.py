from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe que representa as configurações setadas no .env da aplicação.
    """

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encode='utf-8', secrets_dir='.secrets'
    )

    DB_URL: str

    SECURITY_ALGORITHM: str
    SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # SECRETS
    SECURITY_API_SECRET_KEY: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
