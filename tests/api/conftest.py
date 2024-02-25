# mypy: ignore-errors
from fastapi import testclient
import pytest
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext import asyncio as sa

from time_tracker import app, config
from time_tracker.db import database
from time_tracker.db import deps as db_deps
from time_tracker.db import models as db_models


# async connection
async_engine = sa.create_async_engine(database.DATABASE_URL)
TestingAsyncSessionLocal: sa.async_sessionmaker[
    sa.AsyncSession
] = sa.async_sessionmaker(async_engine)


# sync connection
_SETTINGS = config.get_settings()
SYNC_DATABASE_URL = (
    f"postgresql+psycopg2://{_SETTINGS.PG_DB_USER}"  # noqa: E231
    f":{_SETTINGS.PG_DB_PASSWORD}@{_SETTINGS.PG_DB_HOST}/"  # noqa: E231
    f"{_SETTINGS.PG_DB_NAME}"
)
engine = sqlalchemy.create_engine(SYNC_DATABASE_URL)
TestingSessionLocal: orm.sessionmaker[orm.Session] = orm.sessionmaker(engine)


@pytest.fixture(scope="function")
def session():
    with TestingSessionLocal() as sess:
        # clear results of previous tests
        sql = "TRUNCATE {} RESTART IDENTITY;".format(
            ",".join(
                table.name
                for table in reversed(db_models.Base.metadata.sorted_tables)
            )
        )
        sess.execute(sqlalchemy.text(sql))
        sess.commit()
        yield sess


@pytest.fixture(scope="session")
def client():
    async def override_get_session():
        async with TestingAsyncSessionLocal() as sess:
            yield sess

    def override_factory():
        yield TestingAsyncSessionLocal

    app.app.dependency_overrides[db_deps.get_session] = override_get_session
    app.app.dependency_overrides[
        db_deps.get_session_factory
    ] = override_factory

    with testclient.TestClient(app=app.app, base_url="http://test") as client:
        yield client

    del app.app.dependency_overrides[db_deps.get_session]
    del app.app.dependency_overrides[db_deps.get_session_factory]
