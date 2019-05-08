import typing

from typesystem import formats
from typesystem.fields import FORMATS


class TimeFormat(formats.TimeFormat):
    def serialize(self, obj: typing.Any) -> str:
        return obj.isoformat() if obj is not None else None


class DateTimeFormat(formats.DateTimeFormat):
    def serialize(self, obj: typing.Any) -> str:
        if obj is None:
            return None
        value = obj.isoformat()
        if value.endswith("+00:00"):
            value = value[:-6] + "Z"
        return value


FORMATS.update({"datetime": DateTimeFormat(), "time": TimeFormat()})
