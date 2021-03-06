from datetime import datetime
import typing

import orm
import sqlalchemy
from bocadillo import plugin
from databases import Database
from starlette.authentication import SimpleUser

from . import settings
from .contrib.orm.fields import URLField
from .contrib.orm.models import QuerySet
from .contrib.bocadillo.crypto import check_password, make_password

url = settings.TEST_DATABASE_URL if settings.TESTING else settings.DATABASE_URL
database = Database(url, force_rollback=settings.TESTING)
metadata = sqlalchemy.MetaData()


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

    @property
    def is_published(self) -> bool:
        return self.published is not None

    async def update(self, **kwargs) -> None:
        kwargs["modified"] = datetime.now()
        await super().update(**kwargs)

    async def publish(self):
        assert not self.is_published
        await self.update(published=datetime.now())

    async def _get_relative_id(
        self, previous: bool = True
    ) -> typing.Optional[int]:
        if not self.published:
            return None

        filters = {
            "published__lt" if previous else "published__gt": self.published
        }
        order_by = ("-" if previous else "") + "published"

        results = await (
            Post.objects.published_only()
            .filter(**filters)
            .order_by(order_by)
            .all()
        )

        return results[0].id if results else None

    async def get_previous_id(self) -> typing.Optional[int]:
        return await self._get_relative_id(previous=True)

    async def get_next_id(self) -> typing.Optional[int]:
        return await self._get_relative_id(previous=False)


class User(SimpleUser, orm.Model):
    __tablename__ = "users"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    username = orm.String(max_length=200)
    password = orm.String(max_length=200)

    async def check_password(self, password: str) -> bool:
        return await check_password(password, hashed=self.password)

    async def set_password(self, password: str):
        self.password = await make_password(password)


engine = sqlalchemy.create_engine(url)
metadata.create_all(engine)


@plugin
def use_db(app):
    app.on("startup", database.connect)
    app.on("shutdown", database.disconnect)
