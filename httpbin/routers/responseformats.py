# -*- coding: utf-8 -*-
"""Response Formats"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from httpbin.constants import ANGRY_ASCII
from httpbin.constants import ROBOT_TXT
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
async def deflate_encoded_content(request: Request):
    return request_attrs_response(
        request,
        keys=('origin', 'headers', 'method'),
        deflated=True
    )


@router.get(
    '/gzip',
    response_model=RequestDictModel,
    description='Returns GZip-encoded data.',
    response_description='GZip-encoded data.'
)
async def gzip_encoded_content(request: Request):
    """Returns Gzip-encoded data."""
    return request_attrs_response(
        request,
        keys=('origin', 'headers', 'method'),
        gzipped=True
    )


@router.get(
    '/deny',
    response_class=PlainTextResponse,
    description='Returns page denied by robots.txt rules.',
    response_description='Denied message'
)
async def deny_page():
    response = PlainTextResponse(
        content=ANGRY_ASCII,
        status_code=status.HTTP_403_FORBIDDEN
    )
    return response


@router.get(
    '/encoding/utf8',
    response_class=HTMLResponse,
    description='Returns a UTF-8 encoded body.',
    response_description='Encoded UTF-8 content.'
)
async def encoding_utf8():
    # TODO How to set Jinja2Templates
    pass


@router.get(
    '/html',
    response_class=HTMLResponse,
    description='Returns a simple HTML document.',
    response_description='An HTML page.'
)
async def html_page():
    """Returns a simple HTML document."""
    pass


@router.get(
    '/json',
    response_class=JSONResponse,
    description='Returns a simple JSON document.',
    response_description='An JSON document.'
)
async def json_endpoint():
    """Returns a simple JSON document."""
    json_doc = {
        'title': 'Sample Slide Show',
        'date': 'date of publication',
        'author': 'Yours Truly',
        'slides': [
            {'type': 'all', 'title': 'Wake up to WonderWidgets!'},
            {
                'type': 'all',
                'title': 'Overview',
                'items': [
                    'Why <em>WonderWidgets</em> are great',
                    'Who <em>buys</em> WonderWidgets',
                ],
            },
        ],
    }
    return JSONResponse(content=json_doc)


@router.get(
    '/robot.txt',
    response_class=PlainTextResponse,
    description='Returns some robots.txt rules.',
    response_description='Robots file'
)
async def robots_page():
    response = PlainTextResponse(content=ROBOT_TXT)
    return response


@router.get(
    '/xml',
    response_class=Response,
    description='Returns a simple XML document.',
    response_description='An XML document.'
)
async def xml():
    """Returns a simple XML document."""
    # TODO load xml document
    response = Response(media_type='application/xml')
    return response
