import orm
from typesystem.fields import FORMATS

from blogapi.contrib.typesystem import formats


FORMATS.update(
    {
        "datetime": formats.DateTimeFormat(),
        "time": formats.TimeFormat(),
        "url": formats.URLFormat(),
    }
)


class URLField(orm.String):
    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 200)
        super().__init__(format="url", **kwargs)
