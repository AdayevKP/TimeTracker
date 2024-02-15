from sqlalchemy.ext import asyncio as sa

# from sqlalchemy.ext.declarative import declarative_base
from time_tracker import config


_SETTINGS = config.get_settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{_SETTINGS.PG_DB_USER}"  # noqa: E231
    f":{_SETTINGS.PG_DB_PASSWORD}@postgres_db_container/"  # noqa: E231
    f"{_SETTINGS.PG_DB_NAME}"
)

async_engine = sa.create_async_engine(DATABASE_URL)
AsyncSessionLocal: sa.async_sessionmaker[
    sa.AsyncSession
] = sa.async_sessionmaker(async_engine)
# Base = declarative_base()
