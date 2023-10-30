import asyncio
import pathlib
import sys

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))  # isort:skip

from tests.fake_data import FakeUOW


@pytest.fixture(scope="session")
def mock_uow():
    return FakeUOW()


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app(mock_uow) -> FastAPI:
    from main import app

    app.container.account_uow.override(mock_uow)
    return app


@pytest.fixture()
async def client(app) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as test_client:
        yield test_client
