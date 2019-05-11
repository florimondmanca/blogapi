import inspect
import typing
import base64
import binascii

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
)
from starlette.requests import HTTPConnection

AuthResult = typing.Optional[typing.Tuple[AuthCredentials, BaseUser]]


class AuthBackend(AuthenticationBackend):
    def invalid_credentials(self) -> AuthenticationError:
        return AuthenticationError(
            "Could not authenticate with the provided credentials"
        )


class SchemeAuthBackend(AuthBackend):
    scheme: str
    base64_encoded: bool = False

    def get_credentials(self, conn: HTTPConnection) -> typing.Optional[str]:
        if "Authorization" not in conn.headers:
            return None

        auth = conn.headers.get("Authorization")

        try:
            scheme, credentials = auth.split()
        except ValueError:
            raise self.invalid_credentials()

        if scheme.lower() != self.scheme:
            return None

        return self.decode_credentials(credentials)

    def decode_credentials(self, credentials: str) -> str:
        if not self.base64_encoded:
            return credentials

        try:
            return base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise self.invalid_credentials()

    async def authenticate(self, conn: HTTPConnection):
        credentials = self.get_credentials(conn)
        if credentials is None:
            return None

        user = await self.verify(credentials)
        if user is None:
            return None

        return AuthCredentials(["authenticated"]), user

    async def verify(self, credentials: str) -> typing.Optional[BaseUser]:
        raise NotImplementedError


class BasicAuthBackend(SchemeAuthBackend):
    scheme = "basic"

    async def verify(self, credentials: str) -> typing.Optional[BaseUser]:
        username, _, password = credentials.partition(":")
        return await self.check_user(username, password)

    async def check_user(
        self, username: str, password: str
    ) -> typing.Optional[BaseUser]:
        raise NotImplementedError


class TokenAuthBackend(SchemeAuthBackend):
    scheme = "bearer"

    async def verify(self, credentials: str) -> typing.Optional[BaseUser]:
        return await self.check_token(token=credentials)

    async def check_token(self, token: str) -> typing.Optional[BaseUser]:
        raise NotImplementedError


class APIKeyAuthBackend(AuthBackend):
    header = "Api-Key"
    # TODO


class MultiAuthBackend(AuthBackend):
    def __init__(self, backends: typing.List[AuthenticationBackend]):
        self.backends: typing.List[AuthenticationBackend] = [
            backend() if inspect.isclass(backend) else backend
            for backend in backends
        ]

    async def authenticate(self, conn: HTTPConnection) -> AuthResult:
        for backend in self.backends:
            try:
                auth_result = await backend.authenticate(conn)
            except AuthenticationError:
                break

            if auth_result is None:
                continue

            return auth_result

        raise self.invalid_credentials()
