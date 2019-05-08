import pytest


def test_create_post(
    client, post_payload, status_code: int = 201, resp_json: dict = None
):
    resp_json = resp_json if resp_json is not None else {}
    r = client.post("/posts", json=post_payload)
    assert r.status_code == status_code, r.json()
    if status_code == 201:
        assert r.json() == {"id": 1, **post_payload, **resp_json}


@pytest.mark.parametrize("field", ["title"])
def test_if_required_field_missing_then_400(client, post_payload, field):
    del post_payload[field]
    test_create_post(client, post_payload, status_code=400)


@pytest.mark.parametrize("field", ["content"])
def test_if_optional_field_missing_then_ok(client, post_payload, field):
    del post_payload[field]
    test_create_post(client, post_payload, resp_json={"content": ""})
