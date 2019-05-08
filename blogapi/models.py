import databases
import orm
import sqlalchemy

from . import settings

database = databases.Database(str(settings.DATABASE_URL))
metadata = sqlalchemy.MetaData()


class Post(orm.Model):
    __tablename__ = "posts"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    title = orm.String(max_length=300)
    content = orm.Text(allow_blank=True)


engine = sqlalchemy.create_engine(str(settings.DATABASE_URL))
metadata.create_all(engine)
