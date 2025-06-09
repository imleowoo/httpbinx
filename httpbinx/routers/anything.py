from enum import Enum
from os import path

from fastapi import APIRouter, Path
from starlette.requests import Request
from starlette.responses import FileResponse

from httpbinx.helpers import get_bomb_file_path, to_request_info
from httpbinx.schemas import RequestInfo

router = APIRouter(tags=['Anything'])


class BombTypes(str, Enum):
    """The allowed bomb file compression types are: brotli and gzip."""
    brotli = 'brotli'
    gzip = 'gzip'


bombs_path: Path = get_bomb_file_path()


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
    '/bombs/{file}',
    response_class=FileResponse,
    summary='Returns a bomb file.',
    description='**It may cause your client to crash! '
                'References [I use Zip Bombs to Protect my Server](https://idiallo.com/blog/zipbomb-protection)**',
    response_description='Return a bomb for compressed files.'
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
        # dd if=/dev/zero bs=1M count=1000 | gzip -c > bomb-1GB.gz
        return FileResponse(
            path=path.join(bombs_path, 'bomb-1GB.gz'),
            headers={'Content-Encoding': 'gzip'},
        )
    elif file == BombTypes.brotli:
        # dd if=/dev/zero bs=1M count=1000 | brotli > bomb-1GB.br
        return FileResponse(
            path=path.join(bombs_path, 'bomb-1GB.br'),
            headers={'Content-Encoding': 'br'},
        )
    raise ValueError(f'{file} is not a valid file type.')
