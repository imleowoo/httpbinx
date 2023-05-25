# -*- coding: utf-8 -*-
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from httpbinx.helpers import to_request_info
from httpbinx.schemas import RequestAttrs
from httpbinx.schemas import RequestInfo

router = APIRouter(tags=['Request inspection'])


@router.get(
    '/headers',
    response_model=RequestInfo,
    response_model_include={'headers'},
    summary="Return the incoming request's HTTP headers.",
    response_description="The request's headers.",
)
async def headers(request: Request):
    return await to_request_info(request)


@router.get(
    '/ip',
    response_model=RequestInfo,
    response_model_include={'origin'},
    summary="Returns the requester's IP Address.",
    response_description="The Requester's IP Address."
)
async def ip(request: Request):
    return await to_request_info(request)


@router.get(
    '/user-agent',
    summary="Return the incoming requests's User-Agent header.",
    response_description='The request’s User-Agent header.'
)
async def user_agent(request: Request) -> JSONResponse:
    # TODO show_env
    return JSONResponse(
        content={'user-agent': RequestAttrs(request).user_agent}
    )
