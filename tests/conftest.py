import pytest
from bocadillo import configure, create_client

from blogapi import settings

settings.TESTING = True


@pytest.fixture(name="app")
def fixture_app():
    from blogapi.app import app

    configure(app)

    return app


@pytest.fixture(name="client")
def fixture_client(app):
    with create_client(app) as client:
        yield client
