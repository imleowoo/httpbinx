# -*- coding: utf-8 -*-
"""Response Formats"""
import gzip
import zlib

import brotli
from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from httpbinx.constants import ANGRY_ASCII
from httpbinx.constants import ROBOT_TXT
from httpbinx.helpers import get_templates
from httpbinx.helpers import to_request_info
from httpbinx.schemas import RequestInfo

router = APIRouter(tags=['Response formats'])


@router.get(
    '/brotli',
    summary='Returns Brotli-encoded data.',
    response_model=RequestInfo,
    response_class=JSONResponse,
    response_model_include={'origin', 'headers', 'method', 'extras'},
    response_description='Brotli-encoded data.'
)
async def brotli_encoded_content(request: Request):
    info = await to_request_info(request, brotli=True)
    response = JSONResponse(jsonable_encoder(info))
    compressed = brotli.compress(response.body or b'')
    response.body = compressed
    response.headers['Content-Encoding'] = 'br'
    response.headers['Content-Length'] = str(len(compressed))
    return response


@router.get(
    '/deflate',
    summary='Returns Deflate-encoded data.',
    response_model=RequestInfo,
    response_class=JSONResponse,
    response_model_include={'origin', 'headers', 'method', 'extras'},
    response_description='Defalte-encoded data.'
)
async def deflate_encoded_content(request: Request):
    info = await to_request_info(request, deflated=True)
    response = JSONResponse(jsonable_encoder(info))
    obj = zlib.compressobj()
    deflated = obj.compress(response.body or b'')
    deflated += obj.flush()
    response.body = deflated
    response.headers['Content-Encoding'] = 'deflate'
    response.headers['Content-Length'] = str(len(deflated))
    return response


@router.get(
    '/gzip',
    response_model=RequestInfo,
    summary='Returns GZip-encoded data.',
    response_description='GZip-encoded data.'
)
async def gzip_encoded_content(request: Request):
    info = await to_request_info(request, gzipped=True)
    response = JSONResponse(jsonable_encoder(info))
    compressed = gzip.compress(response.body or b'')
    response.body = compressed
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = str(len(compressed))
    return response


@router.get(
    '/deny',
    response_class=PlainTextResponse,
    summary='Returns page denied by robots.txt rules.',
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
    response_class=PlainTextResponse,
    summary='Returns a UTF-8 encoded body.',
    response_description='Encoded UTF-8 content.'
)
async def encoding_utf8():
    # UTF-8 demo content
    with open(file='static/UTF-8-demo.txt', encoding='utf-8') as utf8f:
        return PlainTextResponse(content=utf8f.read())


@router.get(
    '/html',
    response_class=HTMLResponse,
    summary='Returns a simple HTML document.',
    response_description='An HTML page.'
)
async def html_page(
        request: Request,
        templates: Jinja2Templates = Depends(get_templates)
):
    return templates.TemplateResponse(
        'moby.html',
        context={'request': request},
    )


@router.get(
    '/json',
    response_class=JSONResponse,
    summary='Returns a simple JSON document.',
    response_description='An JSON document.'
)
async def json_endpoint():
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
    summary='Returns some robots.txt rules.',
    response_description='Robots file'
)
async def robots_page():
    response = PlainTextResponse(content=ROBOT_TXT)
    return response


@router.get(
    '/xml',
    response_class=Response,
    summary='Returns a simple XML document.',
    response_description='An XML document.'
)
async def xml(
        request: Request,
        templates: Jinja2Templates = Depends(get_templates)
):
    return templates.TemplateResponse(
        'sample.xml',
        context={'request': request},
        media_type='application/xml'
    )
