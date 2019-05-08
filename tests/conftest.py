import pytest
from async_asgi_testclient import TestClient
from bocadillo import App, configure

from blogapi import settings

settings.TESTING = True


@pytest.fixture(autouse=True)
def reset_db():
    from blogapi.models import metadata, engine

    metadata.drop_all(engine)
    metadata.create_all(engine)


@pytest.fixture(name="app", scope="session")
def fixture_app() -> App:
    from blogapi.app import app

    return configure(app, settings)


@pytest.fixture(name="client")
async def fixture_client(app: App):
    async with TestClient(app) as client:
        yield client


@pytest.fixture
def post_payload():
    return {
        "title": "Hello, World",
        "description": "See how beautiful the world is",
        "content": "It's a beautifyl day [...]",
        "image_url": "http://images.net/example",
        "image_caption": "An example image",
    }
