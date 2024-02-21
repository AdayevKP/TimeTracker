# mypy: ignore-errors
import httpx
import pytest
import sqlalchemy

from time_tracker.db import models


@pytest.fixture(scope="function")
async def fill_db(async_session, reset_primary_key):
    async_session.add(models.Project(name="work", description=None))
    async_session.add(
        models.Project(name="study", description="learning math")
    )
    await async_session.commit()
    yield
    await reset_primary_key("projects", "id")


@pytest.mark.usefixtures("fill_db")
async def test_projects_list(client: httpx.AsyncClient):
    response = await client.get("/projects/")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "work", "id": 1, "description": None},
        {"name": "study", "id": 2, "description": "learning math"},
    ]


@pytest.mark.usefixtures("fill_db")
async def test_add_project(client: httpx.AsyncClient, async_session):
    response = await client.post(
        "/projects/",
        json={"name": "MEGA PROJECT", "description": "mega description"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "name": "MEGA PROJECT",
        "id": 3,
        "description": "mega description",
    }

    db_proj = await async_session.execute(
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
async def test_get_project(client: httpx.AsyncClient, proj_id, expected):
    response = await client.get(f"/projects/{proj_id}")
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.usefixtures("fill_db")
async def test_update_project(client: httpx.AsyncClient):
    response = await client.put(
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
    async def test_get_fake_project(self, client: httpx.AsyncClient):
        response = await client.get("/projects/521")
        assert response.status_code == 404

    @pytest.mark.usefixtures("fill_db")
    async def test_update_fake_project(self, client: httpx.AsyncClient):
        response = await client.put(
            "/projects/101",
            json={"name": "work", "description": "working hard"},
        )
        assert response.status_code == 404
