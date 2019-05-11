from bocadillo import App, plugin, HTTPError, settings
from starlette.authentication import AuthenticationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection

from blogapi.contrib.starlette.auth import MultiAuthBackend, AuthResult


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

    # TODO: use `.add_middleware` once Bocadillo supports ASGI-compatible
    # middleware with error handling.
    app.add_asgi_middleware(AuthMiddleware, backend=backend)