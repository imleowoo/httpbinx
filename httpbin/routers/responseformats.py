# -*- coding: utf-8 -*-
"""Response Formats"""
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from starlette import status

from httpbin.constants import ANGRY_ASCII

router = APIRouter()


@router.get('/brotli')
async def brotli_encoded_content():
    """Returns Brotli-encoded data."""
    pass


@router.get('/deflate')
async def deflate_encoded_content():
    """Returns Deflate-encoded data."""
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
