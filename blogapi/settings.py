from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL")
TEST_DATABASE_URL = config("TEST_DATABASE_URL")
TESTING = False
