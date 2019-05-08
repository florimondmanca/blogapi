import pytest

from blogapi.models import Post


NUM_POSTS = 3
EXPECTED_FIELDS = {
    "id",
    "title",
    "content",
    "description",
    "created",
    "modified",
    "published",
    "image_url",
    "image_caption",
}


@pytest.mark.asyncio
async def test_list_posts(client, post_payload):
    for _ in range(NUM_POSTS):
        await Post.objects.create(**post_payload)

    r = await client.get("/posts")
    assert r.status_code == 200
    assert len(r.json()) == NUM_POSTS
    for post in r.json():
        assert set(post) == EXPECTED_FIELDS


@pytest.mark.asyncio
async def test_retrieve_post(client, post_payload):
    post = await Post.objects.create(**post_payload)

    r = await client.get(f"/posts/{post.id}")
    assert r.status_code == 200
    assert r.json() == dict(post, next_id=None, previous_id=None)
