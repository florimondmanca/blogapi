import typing
from starlette_auth_toolkit.backends import BaseBasicAuthBackend
import orm

from .models import User


class BasicAuthBackend(BaseBasicAuthBackend):
    async def verify(
        self, username: str, password: str
    ) -> typing.Optional[User]:
        try:
            user: User = User.objects.get(username=username)
        except orm.exceptions.NoMatch:
            return None

        if await user.check_password(password):
            return user

        return None
