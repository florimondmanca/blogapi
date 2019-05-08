import pytest
from bocadillo import App, configure, create_client

from blogapi import settings

settings.TESTING = True


@pytest.fixture(name="app", scope="session")
def fixture_app() -> App:
    from blogapi.app import app

    return configure(app)


@pytest.fixture(name="client")
def fixture_client(app: App):
    with create_client(app) as client:
        yield client


@pytest.fixture(autouse=True)
def reset_db():
    from blogapi.models import metadata, engine

    metadata.drop_all(engine)
    metadata.create_all(engine)
