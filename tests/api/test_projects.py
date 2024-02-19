import typing as tp

import httpx
import pytest

from time_tracker.db import models


@pytest.fixture(scope="function")
async def fill_db(async_db) -> tp.AsyncIterator[None]:  # type: ignore
    async_db.add(models.Project(name="work", description=None))
    async_db.add(models.Project(name="study", description="learning math"))
    await async_db.commit()
    yield
    # async_db.execute("ALTER SEQUENCE projects_id_seq RESTART WITH 1")
    # async_db.commit()


@pytest.mark.usefixtures("fill_db")
async def test_projects_list(client: httpx.AsyncClient) -> None:
    response = await client.get("/projects/")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "work", "id": 1, "description": None},
        {"name": "study", "id": 2, "description": "learning math"},
    ]


@pytest.mark.usefixtures("fill_db")
async def test_add_project(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/projects/",
        json={"name": "MEGA PROJECT", "description": "mega description"},
    )
    assert response.status_code == 201

    # res = await pgsql.execute(sqlalchemy.text("SELECT * FROM projects"))
    # assert res.fetchall() == [
    #     {
    #         'id': 1, 'name': 'MEGA PROJECT',
    #         'description': 'mega description'
    #     }
    # ]


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
async def test_get_project(client: httpx.AsyncClient, proj_id, expected):  # type: ignore # noqa E501
    response = await client.get(f"/projects/{proj_id}")
    assert response.status_code == 200
    assert response.json() == expected
