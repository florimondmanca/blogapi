import orm
from bocadillo import App, HTTPError

from .models import Post

app = App()


@app.error_handler(orm.exceptions.NoMatch)
async def on_no_match(req, res, exc):
    raise HTTPError(404)


@app.route("/posts")
class PostList:
    async def get(self, req, res):
        res.json = [dict(post) for post in await Post.objects.all()]

    async def post(self, req, res):
        post = await Post.objects.create(**await req.json())
        res.json = dict(post)
        res.status_code = 201


@app.route("/posts/{pk}")
class PostDetail:
    async def get(self, req, res, pk: int):
        post = await Post.objects.get(id=pk)
        res.json = dict(post)

    async def put(self, req, res, pk: int):
        post = await Post.objects.get(id=pk)
        await post.update(**await req.json())
        res.json = dict(post)
