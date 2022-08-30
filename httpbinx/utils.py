# -*- coding: utf-8 -*-
from functools import lru_cache
from os import path


@lru_cache(maxsize=128)
def get_templates_abspath(subdir: str = None) -> str:
    """Return templates' folder abspath
    TODO use Jinja2Templates
    """
    # os.path.join(os.getcwd(), 'httpbin', 'templates')
    templates_abspath = path.join(path.dirname(__file__), 'templates')
    if subdir is None:
        return templates_abspath
    return path.join(templates_abspath, subdir)
