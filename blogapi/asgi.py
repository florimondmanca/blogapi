from bocadillo import configure
from .app import app
from . import settings
from blogapi.contrib.bocadillo import auth

configure(app, settings)
