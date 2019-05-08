import typing


def ignore(d: dict, fields: typing.Sequence[str]) -> dict:
    for field in fields:
        d.pop(field, None)
    return d
