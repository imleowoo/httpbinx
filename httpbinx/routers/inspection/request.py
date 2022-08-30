# -*- coding: utf-8 -*-
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from httpbinx.helpers import request_attrs_response
from httpbinx.schemas import RequestAttrs

router = APIRouter()


@router.get(
    '/headers',
    description="Return the incoming request's HTTP headers.",
    response_description="The request's headers."
)
async def headers(request: Request) -> JSONResponse:
    return request_attrs_response(
        request,
        keys=('headers',)
    )


@router.get(
    '/ip',
    description="Returns the requester's IP Address.",
    response_description="The Requester's IP Address."
)
async def ip(request: Request) -> JSONResponse:
    return request_attrs_response(
        request,
        keys=('origin',)
    )


@router.get('/user-agent')
async def user_agent(request: Request) -> JSONResponse:
    # TODO show_env
    return JSONResponse(
        content={'user-agent': RequestAttrs(request).user_agent}
    )
