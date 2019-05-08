import pytest


@pytest.fixture(name="data")
def fixture_data():
    return {"title": "Hello, World", "content": "Hello, World"}


def test_create_post(
    client, data, status_code: int = 201, resp_json: dict = None
):
    resp_json = resp_json if resp_json is not None else {}
    r = client.post("/posts", json=data)
    assert r.status_code == status_code
    if status_code == 201:
        assert r.json() == {"id": 1, **data, **resp_json}


@pytest.mark.parametrize("field", ["title"])
def test_if_required_field_missing_then_400(client, data, field):
    del data[field]
    test_create_post(client, data, status_code=400)


@pytest.mark.parametrize("field", ["content"])
def test_if_optional_field_missing_then_ok(client, data, field):
    del data[field]
    test_create_post(client, data, resp_json={"content": ""})
