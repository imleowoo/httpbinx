# -*- coding: utf-8 -*-
from fastapi import APIRouter
from starlette.requests import Request

from httpbin.helpers import get_request_attrs

router = APIRouter()


@router.get('/get')
async def get(request: Request):
    return get_request_attrs(
        request,
        keys=("url", "args", "headers", "origin")
    )


@router.post('/post')
async def post(request: Request):
    return get_request_attrs(
        request,
        keys=("url", "args", "form", "data", "origin", "headers", "files", "json")
    )


@router.put('/put')
async def put(request: Request):
    return get_request_attrs(
        request,
        keys=("url", "args", "form", "data", "origin", "headers", "files", "json")
    )


@router.delete('/delete')
async def delete(request: Request):
    return get_request_attrs(
        request,
        keys=('url', 'args', 'form', 'data', 'origin', 'headers', 'files', 'json')
    )


@router.patch('/patch')
async def patch(request: Request):
    return get_request_attrs(
        request,
        keys=("url", "args", "form", "data", "origin", "headers", "files", "json")
    )
