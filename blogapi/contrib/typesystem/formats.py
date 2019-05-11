import typing

from starlette.datastructures import URL
from typesystem import formats


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


class URLFormat(formats.BaseFormat):
    errors = {"invalid": "Must be a valid URL."}

    def is_native_type(self, value: typing.Any) -> bool:
        return False

    def validate(self, value: typing.Any) -> str:
        value = URL(value)
        if not value.scheme or not value.hostname:
            raise self.validation_error("invalid")
        return str(value)

    def serialize(self, obj: typing.Any) -> str:
        return obj
