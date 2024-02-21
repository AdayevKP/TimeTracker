# mypy: ignore-errors
import asyncio
import typing as tp

import httpx
import pytest
import sqlalchemy
from sqlalchemy.ext import asyncio as sa

from time_tracker import app, config
from time_tracker.db import deps as db_deps


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


@pytest.fixture(scope="function")
@pytest.mark.usefixtures("reset_primary_key")
async def async_session(reset_primary_key):
    conn = await async_engine.connect()
    transaction = conn.begin()
    await transaction.start()

    session = TestingAsyncSessionLocal(
        bind=conn, join_transaction_mode="create_savepoint"
    )
    yield session
    await session.commit()
    await session.close()

    # rollback - everything that happened with the
    # Session above (including calls to commit())
    # is rolled back.
    await transaction.rollback()
    # return connection to the Engine
    await conn.close()


@pytest.fixture(scope="function")
async def reset_primary_key():
    reset_name = []

    async def setter(table_name, pk_name):
        reset_name.append((table_name, pk_name))

    yield setter

    async with TestingAsyncSessionLocal() as sess:
        for t, pk in reset_name:
            sql = sqlalchemy.text(
                f"ALTER SEQUENCE {t}_{pk}_seq RESTART WITH 1; "  # noqa: E702
            )
            await sess.execute(sql)
        await sess.commit()


# let test session to know it is running inside event loop
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def engine_conn() -> tp.AsyncGenerator[sa.AsyncConnection, None]:
    async with async_engine.connect() as conn:
        yield conn


@pytest.fixture(scope="function")
async def client(async_session) -> tp.AsyncIterator[httpx.AsyncClient]:
    async def override_get_session():  # type: ignore
        yield async_session

    app.app.dependency_overrides[db_deps.get_session] = override_get_session

    async with httpx.AsyncClient(app=app.app, base_url="http://test") as ac:
        yield ac

    del app.app.dependency_overrides[db_deps.get_session]
