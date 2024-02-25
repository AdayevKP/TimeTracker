# mypy: ignore-errors
from fastapi import testclient
import pytest
import sqlalchemy
from sqlalchemy import orm

from time_tracker.db import models


@pytest.fixture(scope="function")
def fill_db(session: orm.Session):
    session.add(models.Project(name="work", description=None))
    session.add(models.Project(name="study", description="learning math"))
    session.commit()
    yield


@pytest.mark.usefixtures("fill_db")
def test_projects_list(client: testclient.TestClient):
    response = client.get("/projects/")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "work", "id": 1, "description": None},
        {"name": "study", "id": 2, "description": "learning math"},
    ]


@pytest.mark.usefixtures("fill_db")
def test_add_project(client: testclient.TestClient, session: orm.Session):
    response = client.post(
        "/projects/",
        json={"name": "MEGA PROJECT", "description": "mega description"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "name": "MEGA PROJECT",
        "id": 3,
        "description": "mega description",
    }

    db_proj = session.execute(
        sqlalchemy.text("Select * from projects where id = 3")
    )
    proj = db_proj.mappings().first()
    assert proj == {
        "name": "MEGA PROJECT",
        "id": 3,
        "description": "mega description",
    }


@pytest.mark.usefixtures("fill_db")
@pytest.mark.parametrize(
    "proj_id, expected",
    [
        (
            "1",
            {"name": "work", "id": 1, "description": None},
        ),
        ("2", {"name": "study", "id": 2, "description": "learning math"}),
    ],
)
def test_get_project(client: testclient.TestClient, proj_id, expected):
    response = client.get(f"/projects/{proj_id}")
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.usefixtures("fill_db")
def test_update_project(client: testclient.TestClient):
    response = client.put(
        "/projects/1", json={"name": "work", "description": "working hard"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "work",
        "description": "working hard",
    }


class TestErrors:
    @pytest.mark.usefixtures("fill_db")
    def test_get_fake_project(self, client: testclient.TestClient):
        response = client.get("/projects/521")
        assert response.status_code == 404

    @pytest.mark.usefixtures("fill_db")
    def test_update_fake_project(self, client: testclient.TestClient):
        response = client.put(
            "/projects/101",
            json={"name": "work", "description": "working hard"},
        )
        assert response.status_code == 404
