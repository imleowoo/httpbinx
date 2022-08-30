# -*- coding: utf-8 -*-
"""HTTP Methods"""
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from httpbinx.helpers import request_attrs_response
from httpbinx.schemas import RequestDictModel

router = APIRouter()


@router.get(
    '/get',
    response_model=RequestDictModel,
    description="The request's query parameters.",
    response_description="The request's query parameters."
)
async def get(request: Request) -> JSONResponse:
    return request_attrs_response(
        request,
        keys=('url', 'args', 'headers', 'origin')
    )


@router.post(
    '/post',
    response_model=RequestDictModel,
    description="The request's POST parameters.",
    response_description="The request's POST parameters."
)
async def post(request: Request) -> JSONResponse:
    return request_attrs_response(
        request,
        keys=(
            'url', 'args', 'form', 'data', 'origin',
            'headers', 'files', 'json'
        )
    )


@router.put(
    '/put',
    response_model=RequestDictModel,
    description="The request's PUT parameters.",
    response_description="The request's PUT parameters."
)
async def put(request: Request) -> JSONResponse:
    return request_attrs_response(
        request,
        keys=(
            'url', 'args', 'form', 'data', 'origin',
            'headers', 'files', 'json'
        )
    )


@router.delete(
    '/delete',
    response_model=RequestDictModel,
    description="The request's DELETE parameters.",
    response_description="The request's DELETE parameters."
)
async def delete(request: Request) -> JSONResponse:
    return request_attrs_response(
        request,
        keys=(
            'url', 'args', 'form', 'data', 'origin',
            'headers', 'files', 'json'
        )
    )


@router.patch(
    '/patch',
    response_model=RequestDictModel,
    description="The request's PATCH parameters.",
    response_description="The request's PATCH parameters."
)
async def patch(request: Request) -> JSONResponse:
    return request_attrs_response(
        request,
        keys=(
            'url', 'args', 'form', 'data', 'origin',
            'headers', 'files', 'json'
        )
    )
