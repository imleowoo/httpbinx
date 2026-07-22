"""HTTP Request & Response Service, written in Python + FastAPI."""

from .main import app

__version__ = '1.11.0'

app.version = __version__
