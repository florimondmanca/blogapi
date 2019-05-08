import pytest

from blogapi.models import Post

pytestmark = pytest.mark.asyncio


async def test_publish(client, create_post):
    post = await create_post()

    r = await client.post(f"/posts/{post.id}/publication")
    assert r.status_code == 201

    post = await Post.objects.get(id=post.id)
    assert post.is_published

    r = await client.post(f"/posts/{post.id}/publication")
    assert r.status_code == 202
