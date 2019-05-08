import pytest

from blogapi.models import Post

pytestmark = pytest.mark.asyncio


async def test_create_post(
    client, post_payload, status_code: int = 201, resp_json: dict = None
):
    resp_json = resp_json if resp_json is not None else {}
    r = await client.post("/posts", json=post_payload)
    assert r.status_code == status_code, r.json()
    if status_code == 201:
        assert r.json() == {"id": 1, **post_payload, **resp_json}


@pytest.mark.parametrize("field", ["title"])
async def test_if_required_field_missing_then_400(client, post_payload, field):
    del post_payload[field]
    await test_create_post(client, post_payload, status_code=400)


@pytest.mark.parametrize("field", ["content"])
async def test_if_optional_field_missing_then_ok(client, post_payload, field):
    del post_payload[field]
    await test_create_post(client, post_payload, resp_json={"content": ""})


@pytest.mark.parametrize(
    "field, value", [("title", "Title"), ("content", "Content")]
)
async def test_update_post(client, post_payload, field, value):
    post = await Post.objects.create(**post_payload)
    update = {field: value}
    r = await client.put(f"/posts/{post.id}", json=update)
    assert r.status_code == 200
    assert r.json() == {**post, **update}
    post = await Post.objects.get(id=post.id)
    assert post[field] == value
