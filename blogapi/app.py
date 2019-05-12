import orm
from bocadillo import App, HTTPError, view

from .contrib.bocadillo import requires
from .models import Post

app = App()


@app.error_handler(orm.exceptions.NoMatch)
async def on_no_match(req, res, exc):
    raise HTTPError(404)


@app.route("/posts")
class PostList:
    # NOTE: won't work, see contrib/bocadillo/auth.py
    async def get(self, req, res):
        res.json = [dict(post) for post in await Post.objects.all()]

    @requires("authenticated")
    async def post(self, req, res):
        post = await Post.objects.create(**await req.json())
        res.json = dict(post)
        res.status_code = 201


@app.route("/posts/{pk}")
class PostDetail:
    async def get(self, req, res, pk: int):
        post = await Post.objects.get(id=pk)
        res.json = dict(
            post,
            next_id=await post.get_next_id(),
            previous_id=await post.get_previous_id(),
        )

    async def put(self, req, res, pk: int):
        post = await Post.objects.get(id=pk)
        await post.update(**await req.json())
        res.json = dict(post)


@app.route("/posts/{pk}/publication")
@view(methods=["post"])
async def publish(req, res, pk: int):
    post = await Post.objects.get(id=pk)

    if post.is_published:
        res.status_code = 202
    else:
        await post.publish()
        res.status_code = 201

    res.json = dict(post)
