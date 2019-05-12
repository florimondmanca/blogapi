from bocadillo import settings
from passlib.hash import pbkdf2_sha256
from passlib.ifc import PasswordHash
from starlette.concurrency import run_in_threadpool


def get_hasher() -> PasswordHash:
    hasher = settings.get("PASSWORD_HASHER")
    if hasher is None:
        return pbkdf2_sha256
    assert isinstance(hasher, PasswordHash)
    return hasher


async def make_password(password: str) -> str:
    hasher = get_hasher()
    return await run_in_threadpool(hasher.hash, password)


async def check_password(password: str, hashed: str) -> bool:
    hasher = get_hasher()
    return await run_in_threadpool(hasher.verify, password, hashed)
