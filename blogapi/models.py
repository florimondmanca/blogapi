from datetime import datetime

import orm
import sqlalchemy
from bocadillo import plugin
from databases import Database

from . import settings
from . import patches  # pylint: disable=unused-import

url = settings.TEST_DATABASE_URL if settings.TESTING else settings.DATABASE_URL
database = Database(url, force_rollback=settings.TESTING)
metadata = sqlalchemy.MetaData()


class PostQuerySet(orm.models.QuerySet):
    async def create(self, **kwargs) -> "Post":
        kwargs["created"] = kwargs["modified"] = datetime.now()
        return await super().create(**kwargs)


class Post(orm.Model):
    __tablename__ = "posts"
    __database__ = database
    __metadata__ = metadata
    objects = PostQuerySet()

    id = orm.Integer(primary_key=True)
    title = orm.String(max_length=300)
    content = orm.Text(allow_blank=True)
    created = orm.DateTime(index=True)
    modified = orm.DateTime(index=True)
    published = orm.DateTime(allow_null=True)

    async def update(self, **kwargs) -> None:
        kwargs["modified"] = datetime.now()
        await super().update(**kwargs)


engine = sqlalchemy.create_engine(url)


@plugin
def use_db(app):
    metadata.create_all(engine)
    app.on("startup", database.connect)
    app.on("shutdown", database.disconnect)
