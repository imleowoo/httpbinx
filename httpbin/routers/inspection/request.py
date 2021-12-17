from fastapi import APIRouter
from starlette.requests import Request

from httpbin.helpers import get_request_attrs

router = APIRouter()


@router.get('/headers')
async def headers(request: Request):
    return get_request_attrs(
        request,
        keys=('headers',)
    )


@router.get('/ip')
async def ip(request: Request):
    return get_request_attrs(
        request,
        keys=('origin',)
    )


@router.get('/user-agent')
async def user_agent(request: Request):
    pass
