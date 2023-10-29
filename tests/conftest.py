import pytest
from fastapi.testclient import TestClient

from family.services.accounts import AccountService
from main import app
from tests.fake_data import FakeClient, FakeUOW


@pytest.fixture
def mock_uow():
    return FakeUOW()


@pytest.fixture
def client(mock_uow):
    app.container.account_uow.override(mock_uow)
    yield TestClient(app)


@pytest.fixture
def public_service() -> AccountService:
    service = AccountService(FakeUOW(), FakeClient())
    return service
