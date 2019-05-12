from bocadillo import App, plugin, settings
from starlette.authentication import AuthenticationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette_auth_toolkit.backends import MultiAuthBackend
from starlette_auth_toolkit.datatypes import AuthResult
from starlette_auth_toolkit.exceptions import InvalidCredentials

from .errors import HTTPError


def get_default_backend() -> MultiAuthBackend:
    backends = settings.get("AUTH_BACKENDS")
    if backends is None:
        return
    return MultiAuthBackend(backends)


async def authenticate(conn: HTTPConnection) -> AuthResult:
    backend = get_default_backend()
    return await backend.authenticate(conn)


class AuthMiddleware(AuthenticationMiddleware):
    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: AuthenticationError):
        # Let Bocadillo deal with it.
        raise exc from None


@plugin
def use_authentication(app: App) -> None:
    backend = get_default_backend()
    if backend is None:
        return

    @app.error_handler(AuthenticationError)
    async def on_auth_error(req, res, exc):
        raise HTTPError(401, detail=str(exc))

    @app.error_handler(InvalidCredentials)
    async def on_invalid_crendentials(req, res, exc: InvalidCredentials):
        headers = {}
        if exc.scheme.lower() in ("basic", "bearer"):
            headers["WWW-Authenticate"] = exc.scheme.capitalize()
        raise HTTPError(401, detail=str(exc), headers=headers)

    # TODO: use `.add_middleware` once Bocadillo supports ASGI-compatible
    # middleware with error handling.
    app.add_asgi_middleware(AuthMiddleware, backend=backend)
