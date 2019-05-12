import functools
import inspect
import typing

from bocadillo import App, Redirect, Response, WebSocket, plugin
from starlette.requests import HTTPConnection, Request

from .errors import HTTPError


class PermissionDenied(Exception):
    pass


def has_required_scope(
    conn: HTTPConnection, scopes: typing.Sequence[str]
) -> bool:
    for scope in scopes:
        if scope not in conn.auth.scopes:
            return False
    return True


def requires(
    scopes: typing.Union[str, typing.Sequence[str]], redirect: str = None
) -> typing.Callable:
    scopes = [scopes] if isinstance(scopes, str) else list(scopes)

    def decorator(func: typing.Callable) -> typing.Callable:
        protocol = None
        index = None
        sig = inspect.signature(func)
        for idx, parameter in enumerate(sig.parameters.values()):
            if parameter.name not in ("req", "ws"):
                continue
            index = idx
            protocol = {"req": "http", "ws": "websocket"}[parameter.name]
            break
        else:
            raise Exception(f'No "req" or "ws" argument on function "{func}"')

        if protocol == "websocket":

            @functools.wraps(func)
            async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> None:
                websocket: WebSocket = kwargs.get("ws", args[index])
                assert isinstance(websocket, WebSocket)

                if not has_required_scope(websocket, scopes):
                    await websocket.close()
                else:
                    await func(*args, **kwargs)

            return wrapper

        @functools.wraps(func)
        async def async_wrapper(
            *args: typing.Any, **kwargs: typing.Any
        ) -> Response:
            req = kwargs.get("req", args[index])
            assert isinstance(req, Request)

            if not has_required_scope(req, scopes):
                if redirect is not None:
                    raise Redirect(redirect)
                raise PermissionDenied
            return await func(*args, **kwargs)

        return async_wrapper

    return decorator


@plugin
def use_permissions(app: App):
    @app.error_handler(PermissionDenied)
    async def on_permission_denied(req, res, exc):
        raise HTTPError(403)
