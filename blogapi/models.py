from databases import Database
import orm
import sqlalchemy

from . import settings

url = settings.TEST_DATABASE_URL if settings.TESTING else settings.DATABASE_URL

database = Database(url, force_rollback=settings.TESTING)
metadata = sqlalchemy.MetaData()


class Post(orm.Model):
    __tablename__ = "posts"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    title = orm.String(max_length=300)
    content = orm.Text(allow_blank=True)


engine = sqlalchemy.create_engine(url)
metadata.create_all(engine)
