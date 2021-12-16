from starlette.requests import Request


def get_request_attrs(request: Request, *keys, **extras) -> dict:
    """Returns request attrs of given keys"""
    pass
