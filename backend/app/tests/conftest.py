import pytest

from starlette.config import environ
from starlette.testclient import TestClient

from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database

environ['TESTING'] = 'True'

from app.config import get_settings
from app.main import app
from app.database.conf import engine, Base

settings = get_settings()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='module', autouse=True)
def user_token(client):
    data_user = {
        "email": "user@domain.com",
        "password": "password"
    }
    client.post("/api/v1/users", json=data_user)
    response = client.post("/api/v1/token", json=data_user)
    return response.json()


@pytest.fixture(scope='session', autouse=True)
def create_test_database():
    if not database_exists(settings.get_database_url()):
        create_database(settings.get_database_url())
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
