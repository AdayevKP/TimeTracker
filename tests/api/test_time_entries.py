# mypy: ignore-errors
import datetime

from fastapi import testclient
import pytest
import sqlalchemy
from sqlalchemy import orm

from time_tracker.db import models


@pytest.fixture(scope="function")
def project(session: orm.Session):
    proj = models.Project(name="study", description="learning math")
    session.add(proj)
    session.commit()
    session.refresh(proj)
    yield proj.id


@pytest.fixture(scope="function")
def existing_time_entry(session: orm.Session, project):
    entry = models.TimeEntry(
        start_time=datetime.datetime.strptime(
            "2024-02-11 23:00", "%Y-%m-%d %H:%M"
        ),
        end_time=datetime.datetime.strptime(
            "2024-02-12 03:31", "%Y-%m-%d %H:%M"
        ),
        project_id=project,
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    yield entry.id


def test_flow(
    client: testclient.TestClient,
    session: orm.Session,
    project: int,
    existing_time_entry: int,
):
    # create time entry
    resp = client.post(
        "/time_entries/", json={"start_time": "2024-02-14 13:00"}
    )
    assert resp.status_code == 201
    time_entry = resp.json()

    # look at it
    created_entry_id = time_entry["id"]
    resp = client.get(f"/time_entries/{created_entry_id}")
    assert resp.status_code == 200
    assert resp.json() == {
        "id": created_entry_id,
        "start_time": "2024-02-14T13:00:00",
        "end_time": None,
        "project_id": None,
    }

    # look at all entries
    resp = client.get("/time_entries/")
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
    resp = client.put(
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

    db_entry = session.execute(
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
    resp = client.delete(f"/time_entries/{created_entry_id}")
    assert resp.status_code == 200

    db_entry = session.execute(
        sqlalchemy.text(
            f"Select * from time_entries where id = {created_entry_id}"
        )
    )
    entry = db_entry.mappings().first()
    assert entry is None


class TestErrors:
    def test_get_missing(self, client: testclient.TestClient):
        # get non existing entry
        resp = client.get("time_entries/100")
        assert resp.status_code == 404

    def test_delete_missing(self, client: testclient.TestClient):
        resp = client.delete("time_entries/100")
        assert resp.status_code == 404

    def test_update_missing(self, client: testclient.TestClient, project):
        resp = client.put(
            "time_entries/100",
            json={
                "start_time": "2024-02-14 13:00:00",
                "end_time": "2024-02-14 13:31:00",
                "project_id": project,
            },
        )
        assert resp.status_code == 404

    def test_update_with_missing_proj(self, client: testclient.TestClient):
        # update entry with not existing project
        resp = client.put(
            "time_entries/1",
            json={
                "start_time": "2024-02-14T13:00:00",
                "end_time": "2024-02-14T13:31:00",
                "project_id": 5,  # not existed project
            },
        )
        assert resp.status_code == 400

    def test_create_with_missing_proj(self, client: testclient.TestClient):
        resp = client.post(
            "time_entries/",
            json={
                "start_time": "2024-02-14T13:00:00",
                "end_time": "2024-02-14T13:31:00",
                "project_id": 5,
            },
        )
        assert resp.status_code == 400

    def test_start_after_end_time(
        self, client: testclient.TestClient, project
    ):
        resp = client.post(
            "time_entries/",
            json={
                "end_time": "2024-02-14T13:00:00",
                "start_time": "2024-02-14T13:31:00",
                "project_id": project,
            },
        )
        assert resp.status_code == 400
