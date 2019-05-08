import pytest
from blogapi.models import Post


@pytest.fixture(name="post")
def fixture_post(client, post_payload) -> dict:
    r = client.post("/posts", json=post_payload)
    assert r.status_code == 201
    return Post.validate(r.json())


@pytest.mark.parametrize(
    "field, value", [("title", "Title"), ("content", "Content")]
)
def test_update_post(client, post, field, value):
    update = {field: value}
    r = client.put(f"/posts/{post.id}", json=update)
    assert r.status_code == 200
    assert r.json() == {**post, **update}
