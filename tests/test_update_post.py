import pytest

from blogapi.models import Post

pytestmark = pytest.mark.asyncio


@pytest.fixture(name="post")
async def fixture_post(client, post_payload) -> dict:
    r = await client.post("/posts", json=post_payload)
    assert r.status_code == 201
    return Post.validate(r.json())


@pytest.mark.parametrize(
    "field, value", [("title", "Title"), ("content", "Content")]
)
async def test_update_post(client, post, field, value):
    update = {field: value}
    r = await client.put(f"/posts/{post.id}", json=update)
    assert r.status_code == 200
    assert r.json() == {**post, **update}
    post = await Post.objects.get(id=post.id)
    assert post[field] == value
