from datetime import datetime, timedelta

import pytest

from blogapi.models import Post

pytestmark = pytest.mark.asyncio

NAV_FIELDS = ("previous_id", "next_id")


@pytest.fixture(name="create_post")
def fixture_create_post(post_payload):
    async def create(**kwargs):
        kwargs = {**post_payload, **kwargs}
        return await Post.objects.create(**kwargs)

    return create


@pytest.mark.parametrize("field", NAV_FIELDS)
async def test_if_not_published_then_none(client, create_post, field):
    post = await create_post()
    r = await client.get(f"/posts/{post.id}")
    assert r.status_code == 200
    assert r.json()[field] is None


@pytest.mark.parametrize("field", NAV_FIELDS)
async def test_if_published_but_no_relative_then_relative_is_none(
    client, create_post, field
):
    post = await create_post(published=datetime.now())
    r = await client.get(f"/posts/{post.id}")
    assert r.status_code == 200
    assert r.json()[field] is None


@pytest.mark.parametrize(
    "field, delta", zip(NAV_FIELDS, (timedelta(days=-1), timedelta(days=1)))
)
async def test_if_published_and_relative_then_relative_present(
    client, create_post, field, delta
):
    now = datetime.now()
    post = await create_post(published=now)
    relative = await create_post(published=now + delta)

    r = await client.get(f"/posts/{post.id}")
    assert r.status_code == 200
    assert r.json()[field] == relative.id
