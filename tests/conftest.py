import pytest
from bocadillo import App, configure
from async_asgi_testclient import TestClient

from blogapi import settings

settings.TESTING = True


@pytest.fixture(name="app", scope="session")
def fixture_app() -> App:
    from blogapi.app import app

    return configure(app)


@pytest.fixture(name="client")
async def fixture_client(app: App):
    async with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def reset_db():
    from blogapi.models import metadata, engine

    metadata.drop_all(engine)
    metadata.create_all(engine)


@pytest.fixture
def post_payload():
    return {"title": "Hello, World", "content": "Hello, World"}
