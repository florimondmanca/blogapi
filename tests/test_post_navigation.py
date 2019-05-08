import pytest

from blogapi.models import Post

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("field", ("previous", "next"))
async def test_if_not_published_then_none(client, post_payload, field):
    post = await Post.objects.create(**post_payload)
    r = await client.get(f"/posts/{post.id}")
    assert r.status_code == 200
    assert r.json()[field] is None
