from functools import partial

import pytest

from blogapi.models import Post

from .utils import equal_dicts

pytestmark = pytest.mark.asyncio
equal = partial(equal_dicts, ignore=("created", "modified"))


async def create_post(client, post_payload, status_code: int = 201):
    r = await client.post("/posts", json=post_payload)
    assert r.status_code == status_code, r.json()
    return r


async def test_create_post(client, post_payload):
    r = await create_post(client, post_payload, status_code=201)
    assert equal(r.json(), {"id": 1, **post_payload, "published": None})


@pytest.mark.parametrize("field", ["title"])
async def test_if_required_field_missing_then_400(client, post_payload, field):
    del post_payload[field]
    await create_post(client, post_payload, status_code=400)


@pytest.mark.parametrize("field", ["content"])
async def test_if_optional_field_missing_then_ok(client, post_payload, field):
    del post_payload[field]
    r = await create_post(client, post_payload)
    assert equal(
        r.json(), {"id": 1, **post_payload, "content": "", "published": None}
    )


@pytest.mark.parametrize(
    "field, value", [("title", "Title"), ("content", "Content")]
)
async def test_update_post(client, post_payload, field, value):
    post = await Post.objects.create(**post_payload)
    update = {field: value}

    r = await client.put(f"/posts/{post.id}", json=update)
    assert r.status_code == 200

    assert equal(r.json(), {**post, **update})

    post = await Post.objects.get(id=post.id)
    assert post[field] == value
