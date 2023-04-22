import pytest

from starlette.config import environ
from starlette.testclient import TestClient

from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database

from app.tests.users.data import DATA_USER

environ['TESTING'] = 'True'

from app.config import settings
from app.main import app
from app.database.conf import engine, Base


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='module', autouse=True)
def user_token(client):
    client.post("/api/v1/users", json=DATA_USER)
    response = client.post("/api/v1/users/token", json=DATA_USER)
    return response.json()


@pytest.fixture(scope='session', autouse=True)
def create_test_database():
    if not database_exists(settings.database_url):
        create_database(settings.database_url)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
