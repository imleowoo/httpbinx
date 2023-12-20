# -*- coding: utf-8 -*-
"""Dynamic Data"""
import asyncio
import base64
import binascii
import random
import uuid

from fastapi import APIRouter
from fastapi import Path
from fastapi import Query
from fastapi.responses import PlainTextResponse
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.responses import JSONResponse
from starlette.responses import Response
from starlette.responses import StreamingResponse

from httpbinx.constants import AWESOME_BASE64ENCODED
from httpbinx.helpers import to_request_info
from httpbinx.schemas import RequestInfo

router = APIRouter(tags=['Dynamic data'])


class OctetStreamResponse(Response):
    """set response headers Content-Type: application/octet-stream"""
    media_type = 'application/octet-stream'


@router.get(
    '/base64/{value}',
    response_class=PlainTextResponse,
    summary='Decodes base64url-encoded string.',
    response_description='Decoded base64 content.',
)
async def decode_base64(
        value: str = Path(
            ...,
            title='base64-encoded string',
            # examples=[AWESOME_BASE64ENCODED],
            openapi_examples={
                'awesome': {
                    'summary': 'A awesome base64 string',
                    'value': AWESOME_BASE64ENCODED
                }}
        )
):
    encoded: bytes = value.encode('utf-8')
    try:
        decoded = base64.urlsafe_b64decode(encoded).decode('utf-8')
        return PlainTextResponse(content=decoded)
    except binascii.Error as err:
        return PlainTextResponse(
            content=f'Incorrect Base64 data: {value}, err_msg: {err}',
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get(
    '/bytes/{n}',
    response_class=OctetStreamResponse,
    summary='Returns n random bytes generated with given seed',
    response_description='A delayed response.'
)
async def random_bytes(
        n: int = Path(..., title='binary file size', gt=0, lt=100 * 1024),  # set 100KB limit
        seed: int = Query(
            None,
            title='random seed',
            description='Initialize the random number generator'
        )
):
    if seed is not None:
        random.seed(seed)
    # Note: can't just use os.urandom here because it ignores the seed
    # https://docs.python.org/3/library/random.html?highlight=random%20seed#random.seed
    content = bytes(random.randint(0, 255) for _ in range(n))
    return OctetStreamResponse(content=content)  # TODO use StreamingResponse


@router.api_route(
    '/delay/{delay}',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE'],
    response_model=RequestInfo,
    summary='Returns a delayed response (max of 10 seconds).',
    response_description='A delayed response.'
)
async def delay_response(
        *,
        delay: float = Path(..., ge=0, le=10, description='delay seconds'),
        request: Request
):
    await asyncio.sleep(delay)
    return await to_request_info(request)


@router.get(
    '/drip',
    response_class=StreamingResponse,
    summary='Drips data over a duration after an optional initial delay.',
    response_description='A dripped response.'
)
async def drip(
        duration: float = Query(
            default=2,
            description='The amount of time (in seconds) over which to drip each byte'
        ),
        numbytes: int = Query(
            default=10, gt=0, lt=10 * 1024 * 1024,  # set 10MB limit
            description='The number of bytes to respond with',
        ),
        code: int = Query(
            default=200, title='response code',
            description='The response code that will be returned'
        ),
        delay: float = Query(
            default=2, ge=0,
            description='The amount of time (in seconds) to delay before responding'
        ),
):
    await asyncio.sleep(delay)
    # Number of seconds to pause during each data generation
    pause = int(duration / numbytes)

    async def generate_content():
        for _ in range(numbytes):
            yield b'*'
            await asyncio.sleep(pause)

    return StreamingResponse(
        content=generate_content(),
        media_type='application/octet-stream',
        status_code=code
    )


@router.get(
    '/links/{n}/{offset}',
    summary='Generate a page containing n links to other pages which do the same.',
    response_class=HTMLResponse,
    response_description='HTML links.'
)
async def link_page(
        *,
        n: int = Path(
            ..., ge=1, le=200,  # limit to between 1 and 200 links
            description='Number of links'
        ),
        offset: int = Path(..., ge=0),
):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head><title>Links</title></head>
    <body>{body}</body>
    </html>
    """
    body = ''
    link = '<a href="{href}">{text}</a> '
    for i in range(n):
        if i == offset:
            body += f'{i} '
        else:
            body += link.format(
                href=f'/links/{n}/{i}',  # TODO how to use router.url_path_for?
                text=i
            )
    return HTMLResponse(content=html.format(body=body))


@router.get(
    '/range/{numbytes}',
    summary='Streams n random bytes generated with given seed, at given chunk size per packet.',
    response_class=StreamingResponse,
    response_description='Streaming Bytes'
)
async def range_request(
        numbytes: int = Path(
            ..., ge=1, le=100 * 1024,
            description='number of bytes must be in the range (0, 102400]'
        )
):
    raise NotImplementedError


@router.get(
    '/stream-bytes/{n}',
    summary='Streams n random bytes generated with given seed, at given chunk size per packet.',
    response_class=StreamingResponse,
    response_description='Streaming Bytes'
)
async def stream_random_bytes(
        n: int = Path(
            ..., ge=1, le=100 * 1024,  # set 100KB limit
            description='Streams n random bytes generated'
        ),
        seed: int = Query(default=None, ge=0),
        chunk_size: int = Query(default=10 * 1024, ge=1, le=10 * 1024)
):
    if seed is not None:
        random.seed(seed)

    def generate_bytes():
        chunks = bytearray()
        for i in range(n):
            chunks.append(random.randint(0, 255))
            if len(chunks) == chunk_size:
                yield bytes(chunks)
                chunks.clear()
        if chunks:
            yield bytes(chunks)

    return StreamingResponse(content=generate_bytes(), media_type='application/octet-stream')


@router.get(
    '/uuid',
    response_class=JSONResponse,
    summary='Return a UUID4.',
    response_description='A UUID4.'
)
async def get_uuid4():
    out = {'uuid': str(uuid.uuid4())}
    return JSONResponse(content=out)
