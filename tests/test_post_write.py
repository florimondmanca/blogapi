from functools import partial

import pytest

from blogapi.models import Post

from .utils import ignore

pytestmark = pytest.mark.asyncio
normalize = partial(ignore, fields=("created", "modified"))


async def create_post(client, post_payload, status_code: int = 201):
    r = await client.post("/posts", json=post_payload)
    assert r.status_code == status_code
    return r


async def test_create_post(client, post_payload):
    r = await create_post(client, post_payload, status_code=201)
    json = normalize(r.json())
    assert json == {"id": 1, **post_payload, "published": None}


@pytest.mark.parametrize("field", ["title"])
async def test_if_required_field_missing_then_400(client, post_payload, field):
    del post_payload[field]
    await create_post(client, post_payload, status_code=400)


@pytest.mark.parametrize(
    "field, value",
    [
        ("content", ""),
        ("description", ""),
        ("image_url", None),
        ("image_caption", None),
    ],
)
async def test_if_optional_field_missing_then_ok(
    client, post_payload, field, value
):
    del post_payload[field]
    r = await create_post(client, post_payload)
    json = normalize(r.json())
    assert json == {"id": 1, **post_payload, field: value, "published": None}


@pytest.mark.parametrize(
    "field, value", [("title", "Title"), ("content", "Content")]
)
async def test_update_post(client, post_payload, field, value):
    post = await Post.objects.create(**post_payload)
    update = {field: value}

    r = await client.put(f"/posts/{post.id}", json=update)
    assert r.status_code == 200

    json = normalize(r.json())
    expected = normalize({**post, **update})
    assert json == expected

    post = await Post.objects.get(id=post.id)
    assert post[field] == value
