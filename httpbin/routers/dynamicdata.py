"""Dynamic Data"""
import asyncio
import base64
import uuid

from fastapi import APIRouter, Path
from fastapi.responses import PlainTextResponse
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from httpbin.helpers import get_request_attrs

router = APIRouter()


@router.get('/base64/{value}')
async def decode_base64(value: str):
    encoded: bytes = value.encode('utf-8')
    try:
        decoded = base64.urlsafe_b64decode(encoded).decode("utf-8")
        return PlainTextResponse(content=decoded)
    except Exception as err:
        return PlainTextResponse(
            content=f"Incorrect Base64 data try: {value}, err_msg: {err}",
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get('/bytes/{n}')
async def random_bytes(n: int):
    # set 100KB limit
    pass


@router.api_route('/delay/{delay}', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE"])
async def delay_response(*, delay: int = Path(..., ge=0, le=10), request: Request):
    """Returns a delayed response."""
    await asyncio.sleep(delay)
    return get_request_attrs(
        request,
        keys=("url", "args", "form", "data", "origin", "headers", "files")
    )


@router.get('/drip')
async def drip():
    """Drips data over a duration after an optional initial delay."""
    pass


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
    """Streams n random bytes generated with given seed, at given chunk size per packet."""
    pass


@router.get('/stream-bytes/{n}')
async def stream_random_bytes(n: int):
    """Streams n random bytes generated with given seed, at given chunk size per packet."""
    pass


@router.get('/uuid')
async def get_uuid4():
    """Return a UUID4."""
    out = {'uuid': str(uuid.uuid4())}
    return JSONResponse(content=out)
