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
from starlette.responses import JSONResponse

from httpbinx.constants import AWESOME_BASE64ENCODED
from httpbinx.helpers import to_request_info
from httpbinx.responses import OctetStreamResponse
from httpbinx.schemas import RequestInfo

router = APIRouter()


@router.get(
    '/base64/{value}',
    response_class=PlainTextResponse,
    name='Decodes base64url-encoded string.',
    response_description='Decoded base64 content.',
)
async def decode_base64(
        value: str = Path(
            ...,
            title='base64-encoded string',
            example=AWESOME_BASE64ENCODED
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
    name='Returns n random bytes generated with given seed',
    response_description='A delayed response.'
)
async def random_bytes(
        n: int = Path(..., title='binary file size', gt=0, lt=100 * 1024),
        seed: int = Query(
            None,
            title='random seed',
            description='Initialize the random number generator'
        )
):
    # set 100KB limit
    n = min(n, 100 * 1024)
    if seed is not None:
        random.seed(seed)
    # Note: can't just use os.urandom here because it ignores the seed
    # https://docs.python.org/3/library/random.html?highlight=random%20seed#random.seed
    content = bytes(random.randint(0, 255) for _ in range(n))
    return OctetStreamResponse(content=content)


@router.api_route(
    '/delay/{delay}',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE'],
    response_model=RequestInfo,
    name='Returns a delayed response (max of 10 seconds).',
    response_description='A delayed response.'
)
async def delay_response(
        *,
        delay: float = Path(..., ge=0, le=10, description='delay seconds'),
        request: Request
):
    await asyncio.sleep(delay)
    return to_request_info(request)


@router.get(
    '/drip',
    response_class=OctetStreamResponse,
    name='Drips data over a duration after an optional initial delay.',
    response_description='A dripped response.'
)
async def drip(
        duration: float = Query(
            default=2,
            description='The amount of time (in seconds) over which to drip each byte'
        ),
        numbytes: int = Query(
            default=10, gt=0, lt=10 * 1024 * 1024,
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
    content = b''
    for _ in range(numbytes):
        content += b'*'
        await asyncio.sleep(pause)
    return OctetStreamResponse(content=content, status_code=code)


@router.get('/links/{n}/{offset}')
async def link_page(
        *,
        n: int = Path(..., ge=1, le=200),
        offset: int
):
    """Generate a page containing n links to other pages which do the same."""
    pass


@router.get('/range/{numbytes}')
async def range_request(numbytes: int):
    """Streams n random bytes generated with given seed,
    at given chunk size per packet."""
    pass


@router.get('/stream-bytes/{n}')
async def stream_random_bytes(n: int):
    """Streams n random bytes generated with given seed,
    at given chunk size per packet."""
    pass


@router.get('/uuid')
async def get_uuid4():
    """Return a UUID4."""
    out = {'uuid': str(uuid.uuid4())}
    return JSONResponse(content=out)
