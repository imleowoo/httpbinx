# -*- coding: utf-8 -*-
"""HTTP Methods"""
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from httpbin.helpers import request_attrs_response

router = APIRouter()


@router.get(
    '/get',
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
    description="The request's POST parameters.",
    response_description="The request's POST parameters."
)
async def post(request: Request):
    return request_attrs_response(
        request,
        keys=(
            'url', 'args', 'form', 'data', 'origin',
            'headers', 'files', 'json'
        )
    )


@router.put('/put')
async def put(request: Request):
    return request_attrs_response(
        request,
        keys=(
            'url', 'args', 'form', 'data', 'origin',
            'headers', 'files', 'json'
        )
    )


@router.delete('/delete')
async def delete(request: Request):
    return request_attrs_response(
        request,
        keys=(
            'url', 'args', 'form', 'data', 'origin',
            'headers', 'files', 'json'
        )
    )


@router.patch('/patch')
async def patch(request: Request):
    return request_attrs_response(
        request,
        keys=(
            'url', 'args', 'form', 'data', 'origin',
            'headers', 'files', 'json'
        )
    )
