import httpx
import pytest

from time_tracker import app


@pytest.fixture(scope="function")
async def client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=app.app, base_url="http://test") as ac:
        yield ac
