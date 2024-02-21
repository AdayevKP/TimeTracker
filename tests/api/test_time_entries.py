# mypy: ignore-errors
import datetime

import httpx
import pytest
import sqlalchemy
from sqlalchemy.ext import asyncio as sa

from time_tracker.db import models


@pytest.fixture(scope="function")
async def project(async_session, reset_primary_key):
    proj = models.Project(name="study", description="learning math")
    async_session.add(proj)
    await async_session.commit()
    await async_session.refresh(proj)
    yield proj.id
    await reset_primary_key("projects", "id")


@pytest.fixture(scope="function")
async def existing_time_entry(async_session, reset_primary_key, project):

    entry = models.TimeEntry(
        start_time=datetime.datetime.strptime(
            "2024-02-11 23:00", "%Y-%m-%d %H:%M"
        ),
        end_time=datetime.datetime.strptime(
            "2024-02-12 03:31", "%Y-%m-%d %H:%M"
        ),
        project_id=project,
    )
    async_session.add(entry)
    await async_session.commit()
    await async_session.refresh(entry)
    yield entry.id
    await reset_primary_key("time_entries", "id")


async def test_flow(
    client: httpx.AsyncClient,
    async_session: sa.AsyncSession,
    project: int,
    existing_time_entry: int,
):
    # create time entry
    resp = await client.post(
        "/time_entries/", json={"start_time": "2024-02-14 13:00"}
    )
    assert resp.status_code == 201
    time_entry = resp.json()

    # look at it
    created_entry_id = time_entry["id"]
    resp = await client.get(f"/time_entries/{created_entry_id}")
    assert resp.status_code == 200
    assert resp.json() == {
        "id": created_entry_id,
        "start_time": "2024-02-14T13:00:00",
        "end_time": None,
        "project_id": None,
    }

    # look at all entries
    resp = await client.get("/time_entries/")
    assert resp.status_code == 200
    assert resp.json() == [
        {
            "id": existing_time_entry,
            "start_time": "2024-02-11T23:00:00",
            "end_time": "2024-02-12T03:31:00",
            "project_id": project,
        },
        {
            "id": created_entry_id,
            "start_time": "2024-02-14T13:00:00",
            "end_time": None,
            "project_id": None,
        },
    ]

    # stop timer and add project to your time entry
    resp = await client.put(
        f"/time_entries/{created_entry_id}",
        json={
            **time_entry,
            "end_time": "2024-02-14 13:31",
            "project_id": project,
        },
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "id": created_entry_id,
        "start_time": "2024-02-14T13:00:00",
        "end_time": "2024-02-14T13:31:00",
        "project_id": project,
    }

    db_entry = await async_session.execute(
        sqlalchemy.text(
            f"Select * from time_entries where id = {created_entry_id}"
        )
    )
    entry = db_entry.mappings().first()
    assert entry == {
        "id": created_entry_id,
        "start_time": datetime.datetime.strptime(
            "2024-02-14 13:00", "%Y-%m-%d %H:%M"
        ),
        "end_time": datetime.datetime.strptime(
            "2024-02-14 13:31", "%Y-%m-%d %H:%M"
        ),
        "project_id": 1,
    }

    # delete
    resp = await client.delete(f"/time_entries/{created_entry_id}")
    assert resp.status_code == 200

    db_entry = await async_session.execute(
        sqlalchemy.text(
            f"Select * from time_entries where id = {created_entry_id}"
        )
    )
    entry = db_entry.mappings().first()
    assert entry is None


class TestErrors:
    async def test_get_missing(self, client: httpx.AsyncClient):
        # get non existing entry
        resp = await client.get("time_entries/100")
        assert resp.status_code == 404

    async def test_delete_missing(self, client: httpx.AsyncClient):
        resp = await client.delete("time_entries/100")
        assert resp.status_code == 404

    async def test_update_missing(self, client: httpx.AsyncClient, project):
        resp = await client.put(
            "time_entries/100",
            json={
                "start_time": "2024-02-14 13:00:00",
                "end_time": "2024-02-14 13:31:00",
                "project_id": project,
            },
        )
        assert resp.status_code == 404

    async def test_update_with_missing_proj(self, client: httpx.AsyncClient):
        # update entry with not existing project
        resp = await client.put(
            "time_entries/1",
            json={
                "start_time": "2024-02-14T13:00:00",
                "end_time": "2024-02-14T13:31:00",
                "project_id": 5,  # not existed project
            },
        )
        assert resp.status_code == 400

    async def test_create_with_missing_proj(self, client: httpx.AsyncClient):
        resp = await client.post(
            "time_entries/",
            json={
                "start_time": "2024-02-14T13:00:00",
                "end_time": "2024-02-14T13:31:00",
                "project_id": 5,
            },
        )
        assert resp.status_code == 400

    async def test_start_after_end_time(
        self, client: httpx.AsyncClient, project
    ):
        resp = await client.post(
            "time_entries/",
            json={
                "end_time": "2024-02-14T13:00:00",
                "start_time": "2024-02-14T13:31:00",
                "project_id": project,
            },
        )
        assert resp.status_code == 400
