from sqlalchemy.ext import asyncio as sa_async
from sqlalchemy.ext.declarative import declarative_base

from app import config

_SETTINGS = config.get_settings()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{_SETTINGS.PG_DB_USER}:{_SETTINGS.PG_DB_PASSWORD}@postgres_db_container/{_SETTINGS.PG_DB_NAME}"
)

async_engine = sa_async.create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = sa_async.async_sessionmaker(async_engine)
# Base = declarative_base()
