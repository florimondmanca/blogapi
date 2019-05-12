from bocadillo import configure
from .app import app
from . import settings, auth

configure(app, settings)
