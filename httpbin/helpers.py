import json

from starlette.requests import Request
from starlette.responses import Response
from starlette import status

from httpbin.schemas import RequestDictModel, RequestAttrs
from httpbin.constants import REDIRECT_LOCATION, ACCEPTED_MEDIA_TYPES, ASCII_ART


def get_request_attrs(request: Request, keys, **extras) -> dict:
    """Returns request attrs of given keys"""
    properties = RequestDictModel.get_properties()
    assert all(map(properties.__contains__, keys))

    request_attrs = RequestAttrs(request=request)

    request_dict = RequestDictModel(
        url=request_attrs.url,
        args=request_attrs.args,
        form=request_attrs.form,
        data=request_attrs.data,
        headers=request_attrs.headers,
        origin=request_attrs.client_host,
        files=request_attrs.files,
        json_data=request_attrs.json,
        method=request_attrs.method
    ).dict(include=set(keys))
    return request_dict


def status_code(code: int):
    """Returns response object of given status code."""
    # sample redirect
    redirect = dict(headers=dict(location=REDIRECT_LOCATION))

    # https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status
    code_map = {
        status.HTTP_301_MOVED_PERMANENTLY: redirect,
        status.HTTP_302_FOUND: redirect,
        status.HTTP_303_SEE_OTHER: redirect,
        status.HTTP_304_NOT_MODIFIED: dict(data=''),
        status.HTTP_305_USE_PROXY: redirect,
        status.HTTP_307_TEMPORARY_REDIRECT: redirect,
        status.HTTP_401_UNAUTHORIZED: dict(
            headers={'WWW-Authenticate': 'Basic realm="Fake Realm"'}
        ),
        status.HTTP_402_PAYMENT_REQUIRED: dict(
            data='Fuck you, pay me!',
            headers={'x-more-info': 'http://vimeo.com/22053820'}
        ),
        status.HTTP_406_NOT_ACCEPTABLE: dict(data=json.dumps({
            'message': 'Client did not request a supported media type.',
            'accept': ACCEPTED_MEDIA_TYPES
        }),
            headers={'Content-Type': 'application/json'}),
        status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED: dict(headers={'Proxy-Authenticate': 'Basic realm="Fake Realm"'}),
        status.HTTP_408_REQUEST_TIMEOUT: dict(  # I'm a teapot!
            data=ASCII_ART,
            headers={'x-more-info': 'http://tools.ietf.org/html/rfc2324'}
        ),
    }

    resp = Response(status_code=code)
    if code in code_map:
        pass
    return resp
