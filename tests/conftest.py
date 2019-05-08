import pytest
from blogapi import settings
from bocadillo import configure, create_client

settings.DATABASE_URL = "sqlite://:memory:"


@pytest.fixture(name="app")
def fixture_app():
    from blogapi.app import app

    configure(app)
    return app


@pytest.fixture
def client(app):
    return create_client(app)
