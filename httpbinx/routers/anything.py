from enum import Enum
from os import path

from fastapi import APIRouter, Path
from starlette.requests import Request
from starlette.responses import FileResponse

from httpbinx.helpers import to_request_info
from httpbinx.schemas import RequestInfo

router = APIRouter(tags=['Anything'])


class BombTypes(str, Enum):
    """The allowed bomb file compression types are: brotli, deflate, and gzip."""
    brotli = 'brotli'
    deflate = 'deflate'
    gzip = 'gzip'


bombs_path = path.join('static', 'bombs')


@router.api_route(
    '/anything',  # TODO path regex
    response_model=RequestInfo,
    summary='Returns anything passed in request data.',
    response_description='Anything passed in request',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE']
)
async def anything(request: Request):
    return await to_request_info(request)


@router.get(
    '/bombs/{file}'
)
async def bomb_file(
    *,
    file: BombTypes = Path(
        ...,
        title='Compression types',
        description='The allowed bomb file compression types',
    )
):
    if file == BombTypes.gzip:
        return FileResponse(
            path=path.join(bombs_path, 'bomb-1GB.gz'),
            headers={'Content-Encoding': 'gzip'},
        )
    elif file == BombTypes.brotli:
        return FileResponse(
            path=path.join(bombs_path, 'bomb-1GB.br'),
            headers={'Content-Encoding': 'br'},
        )
    elif file == BombTypes.deflate:
        return FileResponse(
            path=path.join(bombs_path, 'bomb-1GB.deflate'),
            headers={'Content-Encoding': 'deflate'},
        )
