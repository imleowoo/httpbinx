# -*- coding: utf-8 -*-
# flake8: noqa
import pkgutil

from .main import app

__version__ = (pkgutil.get_data(__package__, 'VERSION') or b'').decode('ascii').strip()
version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))

del pkgutil

app.version = __version__
