import orm

__all__ = ["URLField"]


class URLField(orm.String):
    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 200)
        super().__init__(format="url", **kwargs)
