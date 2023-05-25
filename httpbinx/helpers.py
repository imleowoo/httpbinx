# -*- coding: utf-8 -*-
import json
import random
import re

from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates

from httpbinx.constants import ACCEPTED_MEDIA_TYPES
from httpbinx.constants import ASCII_ART
from httpbinx.constants import REDIRECT_LOCATION
from httpbinx.schemas import RequestAttrs
from httpbinx.schemas import RequestInfo

# init Jinja2
_templates = Jinja2Templates(directory='templates')


def get_templates() -> Jinja2Templates:
    """Dependency function that creates and returns a Jinja2 templates instance"""
    return _templates


async def to_request_info(request: Request, **extras) -> RequestInfo:
    """Returns model RequestInfo instance"""
    await request.body()  # Note: Execute `.stream()` only once.
    attrs = RequestAttrs(request=request)
    info = await attrs.request_info()
    if extras:
        info.extras.update(extras)
    return info


def status_code_response(code: int) -> Response:
    """Returns response object of given status code."""
    # sample redirect
    redirect = dict(headers=dict(location=REDIRECT_LOCATION))

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
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
            headers={'x-more-info': 'https://vimeo.com/22053820'}
        ),
        status.HTTP_406_NOT_ACCEPTABLE: dict(
            data=json.dumps({
                'message': 'Client did not request a supported media type.',
                'accept': ACCEPTED_MEDIA_TYPES
            }),
            headers={'Content-Type': 'application/json'}),
        status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED: dict(
            headers={'Proxy-Authenticate': 'Basic realm="Fake Realm"'}
        ),
        status.HTTP_418_IM_A_TEAPOT: dict(  # I'm a teapot!
            data=ASCII_ART,
            headers={'x-more-info': 'https://datatracker.ietf.org/doc/html/rfc2324'}
        ),
    }

    resp = Response(status_code=code)
    if code in code_map:
        m = code_map[code]
        if 'data' in m:
            resp.body = resp.render(m['data'])
        if 'headers' in m:
            resp.init_headers(m['headers'])

    return resp


def check_basic_auth(request: Request, user: str, password: str):
    """Checks user authentication using HTTP Basic Auth."""
    pass


def weighted_choice(choices):
    """Returns a value from choices chosen by weighted random selection
    choices should be a list of (value, weight) tuples.

    Examples:
        weighted_choice([('val1', 5), ('val2', 0.3), ('val3', 1)])
    """
    values, weights = zip(*choices)
    # TODO Use the `bisect.bisect` method as in the postmanlabs/httpbin project.
    value = random.choices(population=values, weights=weights, k=1)[0]
    return value


def parse_multi_value_header(header_value: str) -> list:
    """Break apart an HTTP header string that is potentially a quoted,
    comma separated list as used in entity headers in RFC2616."""
    parsed_parts = []
    if header_value:
        parts = header_value.split(',')
        for part in parts:
            # TODO
            match = re.search(r'\s*(W/)?\"?([^"]*)\"?\s*', part)
            if match is not None:
                parsed_parts.append(match.group(2))
    return parsed_parts
