# -*- coding: utf-8 -*-
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from httpbinx.helpers import request_attrs_response, get_request_attrs, get_request_info
from httpbinx.schemas import RequestAttrs, RequestInfo

router = APIRouter()


@router.get(
    '/headers',
    response_model=RequestInfo,
    response_model_include={'headers'},
    name="Return the incoming request's HTTP headers.",
    response_description="The request's headers.",
)
async def headers(request: Request):
    return get_request_info(request)


@router.get(
    '/ip',
    name="Returns the requester's IP Address.",
    response_description="The Requester's IP Address."
)
async def ip(request: Request) -> JSONResponse:
    return request_attrs_response(
        request,
        keys=('origin',)
    )


@router.get(
    '/user-agent',
    name="Return the incoming requests's User-Agent header.",
    response_description='The request’s User-Agent header.'
)
async def user_agent(request: Request) -> JSONResponse:
    # TODO show_env
    return JSONResponse(
        content={'user-agent': RequestAttrs(request).user_agent}
    )
