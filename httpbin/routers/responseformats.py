# -*- coding: utf-8 -*-
"""Response Formats"""
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from starlette import status
from starlette.requests import Request

from httpbin.constants import ANGRY_ASCII
from httpbin.helpers import request_attrs_response
from httpbin.schemas import RequestDictModel

router = APIRouter()


@router.get(
    '/brotli',
    response_model=RequestDictModel,
    description='Returns Brotli-encoded data.',
    response_description='Brotli-encoded data.'
)
async def brotli_encoded_content(request: Request):
    return request_attrs_response(
        request,
        keys=('origin', 'headers', 'method'),
        brotli=True
    )


@router.get(
    '/deflate',
    response_model=RequestDictModel,
    description='Returns Deflate-encoded data.',
    response_description='Defalte-encoded data.'
)
async def deflate_encoded_content():
    pass


@router.get('/gzip')
async def gzip_encoded_content():
    """Returns Gzip-encoded data."""
    pass


@router.get('/deny')
async def deny_page():
    """Returns page denied by robots.txt rules."""
    response = PlainTextResponse(
        content=ANGRY_ASCII,
        status_code=status.HTTP_403_FORBIDDEN
    )
    return response


@router.get('/encoding/utf8')
async def encoding_utf8():
    """Returns a UTF-8 encoded body."""
    pass


@router.get('/html')
async def html_page():
    """Returns a simple HTML document."""
    pass


@router.get('/json')
async def json_endpoint():
    """Returns a simple JSON document."""
    pass


@router.get('/robot.txt')
async def robots_page():
    """Returns some robots.txt rules."""
    pass


@router.get('/xml')
async def xml():
    """Returns a simple XML document."""
    pass
