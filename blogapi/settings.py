from starlette.config import Config

config = Config(".env")

TESTING = False

DATABASE_URL = config("DATABASE_URL")
TEST_DATABASE_URL = config("TEST_DATABASE_URL")

ALLOWED_HOSTS = ["localhost", "*.florimond.dev"]

CORS = {
    "allow_origins": ["http://localhost:4200", "https://blog.florimond.dev"],
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
