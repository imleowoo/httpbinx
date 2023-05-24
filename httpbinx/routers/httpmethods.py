# -*- coding: utf-8 -*-
"""HTTP Methods"""
from fastapi import APIRouter
from starlette.requests import Request

from httpbinx.helpers import to_request_info
from httpbinx.schemas import RequestInfo

router = APIRouter(tags=['HTTP Methods'])


@router.get(
    '/get',
    response_model=RequestInfo,
    response_model_include={'url', 'args', 'headers', 'origin'},
    summary="The request's query parameters.",
    response_description="The request's query parameters."
)
async def get(request: Request):
    return await to_request_info(request)


@router.post(
    '/post',
    response_model=RequestInfo,
    summary="The request's POST parameters.",
    response_description="The request's POST parameters."
)
async def post(request: Request):
    return await to_request_info(request)


@router.put(
    '/put',
    response_model=RequestInfo,
    summary="The request's PUT parameters.",
    response_description="The request's PUT parameters."
)
async def put(request: Request):
    return await to_request_info(request)


@router.delete(
    '/delete',
    response_model=RequestInfo,
    summary="The request's DELETE parameters.",
    response_description="The request's DELETE parameters."
)
async def delete(request: Request):
    return await to_request_info(request)


@router.patch(
    '/patch',
    response_model=RequestInfo,
    summary="The request's PATCH parameters.",
    response_description="The request's PATCH parameters."
)
async def patch(request: Request):
    return await to_request_info(request)
