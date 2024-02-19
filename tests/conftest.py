import asyncio
import typing as tp

import httpx
import pytest
import sqlalchemy
from sqlalchemy.ext import asyncio as sa

# from sqlalchemy.ext.declarative import declarative_base
from time_tracker import app, config
from time_tracker.db import deps as db_deps
from time_tracker.db import models as db_models


_SETTINGS = config.get_settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{_SETTINGS.PG_DB_USER}"  # noqa: E231
    f":{_SETTINGS.PG_DB_PASSWORD}@postgres_db_container/"  # noqa: E231
    f"{_SETTINGS.PG_DB_NAME}"
)

async_engine = sa.create_async_engine(DATABASE_URL)
TestingAsyncSessionLocal: sa.async_sessionmaker[
    sa.AsyncSession
] = sa.async_sessionmaker(async_engine, autocommit=False, autoflush=False)


async def override_get_session():  # type: ignore
    async with TestingAsyncSessionLocal() as sess:
        yield sess


app.app.dependency_overrides[db_deps.get_session] = override_get_session


# @pytest.fixture(scope='session')
# async def async_db_engine():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(db_models.Base.metadata.drop_all)
#         await conn.run_sync(db_models.Base.metadata.create_all)


# truncate all table to isolate tests
@pytest.fixture(scope="function")
async def async_db():  # type: ignore
    async with TestingAsyncSessionLocal() as session:
        await session.begin()
        yield session
        await session.rollback()

        for table in db_models.Base.metadata.tables.values():
            print(table)
            await session.execute(
                sqlalchemy.text(f"TRUNCATE TABLE {table} cascade")
            )
        await session.commit()


# let test session to know it is running inside event loop
@pytest.fixture(scope="session")
def event_loop():  # type: ignore
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def engine_conn() -> tp.AsyncGenerator[sa.AsyncConnection, None]:
    async with async_engine.connect() as conn:
        yield conn


@pytest.fixture(scope="session")
async def client() -> tp.AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app.app, base_url="http://test") as ac:
        yield ac
