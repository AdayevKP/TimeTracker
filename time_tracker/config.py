from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PG_DB_NAME: str
    PG_DB_USER: str
    PG_DB_PASSWORD: str
    PG_DB_PORT: str
    PG_DB_HOST: str

    model_config = SettingsConfigDict(env_file="./.env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
