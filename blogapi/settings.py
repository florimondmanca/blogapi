from starlette.config import Config
from starlette.datastructures import URL

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=URL)
