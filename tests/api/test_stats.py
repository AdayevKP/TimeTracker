# mypy: ignore-errors
import datetime

from fastapi import testclient
import freezegun
import pytest
from sqlalchemy import orm

from time_tracker.db import models


@pytest.fixture(scope="function")
def fill_db(session: orm.Session):
    session.add_all(
        [
            models.Project(name="study", description="learning math"),
            models.Project(name="work", description="working"),
        ]
    )
    session.add_all(
        [
            models.TimeEntry(
                start_time=datetime.datetime.strptime(
                    "2024-02-13 01:00", "%Y-%m-%d %H:%M"
                ),
                end_time=datetime.datetime.strptime(
                    "2024-02-13 03:30", "%Y-%m-%d %H:%M"
                ),
                project_id=1,
            ),  # entry in the middle of the week
            models.TimeEntry(
                start_time=datetime.datetime.strptime(
                    "2024-02-11 23:00", "%Y-%m-%d %H:%M"
                ),
                end_time=datetime.datetime.strptime(
                    "2024-02-12 03:00", "%Y-%m-%d %H:%M"
                ),
                project_id=2,
            ),  # entry on the week edge
            models.TimeEntry(
                start_time=datetime.datetime.strptime(
                    "2024-02-18 22:30", "%Y-%m-%d %H:%M"
                ),
                end_time=datetime.datetime.strptime(
                    "2024-02-19 01:00", "%Y-%m-%d %H:%M"
                ),
                project_id=1,
            ),  # second entry on the week edge
            models.TimeEntry(
                start_time=datetime.datetime.strptime(
                    "2024-02-13 16:45", "%Y-%m-%d %H:%M"
                ),
                end_time=datetime.datetime.strptime(
                    "2024-02-13 18:45", "%Y-%m-%d %H:%M"
                ),
                project_id=None,
            ),  # no project entry
        ]
    )
    session.commit()
    yield


@freezegun.freeze_time("2024-02-14")
def test_empty_stats(client: testclient.TestClient):
    resp = client.post("/statistics/", json={"scale": "week"})
    assert resp.status_code == 200
    assert resp.json() == {
        "total_time": "0:00:00",
        "time_per_day": {
            "2024-02-12": "0:00:00",
            "2024-02-13": "0:00:00",
            "2024-02-14": "0:00:00",
            "2024-02-15": "0:00:00",
            "2024-02-16": "0:00:00",
            "2024-02-17": "0:00:00",
            "2024-02-18": "0:00:00",
        },
        "time_per_project": [],
    }


@freezegun.freeze_time("2024-02-18")
@pytest.mark.usefixtures("fill_db")
def test_get_stats(client: testclient.TestClient):
    resp = client.post("/statistics/", json={"scale": "week"})
    assert resp.status_code == 200
    assert resp.json() == {
        "total_time": "9:00:00",
        "time_per_day": {
            "2024-02-12": "3:00:00",
            "2024-02-13": "4:30:00",
            "2024-02-14": "0:00:00",
            "2024-02-15": "0:00:00",
            "2024-02-16": "0:00:00",
            "2024-02-17": "0:00:00",
            "2024-02-18": "1:30:00",
        },
        "time_per_project": [
            {"project_id": 1, "time": "4:00:00"},
            {"project_id": 2, "time": "3:00:00"},
            {"project_id": None, "time": "2:00:00"},
        ],
    }
