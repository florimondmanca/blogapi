import pytest


@pytest.fixture
def data():
    return {"title": "Hello, World", "content": "Hello, World"}


def test_create_post(client, data):
    r = client.post("/posts", json=data)
    assert r.status_code == 201, r.json()
    assert r.json() == {"id": 1, **data}
