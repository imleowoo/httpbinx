# -*- coding: utf-8 -*-
from email.utils import formatdate
import uuid

from fastapi import APIRouter
from fastapi import Path
from starlette import status
from starlette.requests import Request

from httpbinx.helpers import parse_multi_value_header
from httpbinx.helpers import status_code_response
from httpbinx.routers import httpmethods

router = APIRouter(tags=['Response inspection'],)


@router.get(
    '/cache',
    summary='Returns a 304 if an If-Modified-Since header or If-None-Match'
            ' is present. Returns the same as a GET otherwise.',
    response_description='TODO'
)
async def cache(request: Request):
    # https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/If-Modified-Since
    is_conditional = request.headers.get('If-Modified-Since') or \
                     request.headers.get('If-None-Match')
    if is_conditional is None:
        response = await httpmethods.get(request)
        response.headers['Last-Modified'] = formatdate()
        response.headers['ETag'] = uuid.uuid4().hex
        return response
    else:
        return status_code_response(status.HTTP_304_NOT_MODIFIED)


@router.get(
    '/cache/{value}',
    summary='Sets a Cache-Control header for n seconds.',
    response_description='Cache control set'
)
async def cache_control(
        *,
        value: int = Path(..., title='Cache-Control max-age value'),
        request: Request
):
    response = await httpmethods.get(request)
    response.headers['Cache-Control'] = f'public, max-age={value}'
    return response


@router.get(
    '/etag/{etag}',
    summary='Assumes the resource has the given etag and responds '
            'to If-None-Match and If-Match headers appropriately.',
)
async def set_etag(
        *,
        etag: str = Path(..., title='ETag value'),
        request: Request
):
    # TODO set If-None-Match
    # https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/If-None-Match
    if_none_match = parse_multi_value_header(
        request.headers.get('If-None-Match')
    )
    if_match = parse_multi_value_header(request.headers.get('If-Match'))

    if if_none_match:
        if etag in if_none_match or '*' in if_none_match:
            response = status_code_response(status.HTTP_304_NOT_MODIFIED)
            response.headers['ETag'] = etag
            return response
    elif if_match:
        if etag not in if_match and '*' not in if_match:
            return status_code_response(status.HTTP_412_PRECONDITION_FAILED)
    # Special cases don't apply, return normal response
    response = await httpmethods.get(request)
    response.headers['ETag'] = etag
    return response


@router.api_route(
    '/response-headers',
    summary='Returns a set of response headers from the query string.',
    response_description='Response headers'
)
async def response_headers(
        request: Request
):
    pass
