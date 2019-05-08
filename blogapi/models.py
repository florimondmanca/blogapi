from datetime import datetime
import typing

import orm
import sqlalchemy
from bocadillo import plugin
from databases import Database

from . import settings
from .contrib import URLField, QuerySet

url = settings.TEST_DATABASE_URL if settings.TESTING else settings.DATABASE_URL
database = Database(url, force_rollback=settings.TESTING)
metadata = sqlalchemy.MetaData()


def prepare_order_args(order_args):
    from sqlalchemy.sql import text

    return [text(arg) for arg in order_args]


class PostQuerySet(QuerySet):
    async def create(self, **kwargs) -> "Post":
        kwargs["created"] = kwargs["modified"] = datetime.now()
        return await super().create(**kwargs)

    def published_only(self) -> "PostQuerySet":
        return self.filter(published__isnot=None)


class Post(orm.Model):
    __tablename__ = "posts"
    __database__ = database
    __metadata__ = metadata
    objects = PostQuerySet()

    id = orm.Integer(primary_key=True)

    title = orm.String(max_length=300)
    description = orm.Text(allow_blank=True)  # Social cards and RSS
    content = orm.Text(allow_blank=True)

    created = orm.DateTime(index=True)
    modified = orm.DateTime(index=True)
    published = orm.DateTime(allow_null=True)

    image_url = URLField(allow_null=True)
    image_caption = orm.Text(allow_null=True)

    async def update(self, **kwargs) -> None:
        kwargs["modified"] = datetime.now()
        await super().update(**kwargs)

    async def _find_published(self, order_by, **filters):
        if not self.published:
            return None
        qs = await (
            Post.objects.published_only()
            .filter(**filters)
            .order_by(order_by)
            .all()
        )
        return qs[0].id if qs else None

    async def get_previous_id(self) -> typing.Optional["Post"]:
        return await self._find_published(
            "published desc", published__lt=self.published
        )

    async def get_next_id(self) -> typing.Optional["Post"]:
        return await self._find_published(
            "published", published__gt=self.published
        )


engine = sqlalchemy.create_engine(url)
metadata.create_all(engine)


@plugin
def use_db(app):
    app.on("startup", database.connect)
    app.on("shutdown", database.disconnect)
