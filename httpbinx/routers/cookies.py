# -*- coding: utf-8 -*-
"""Cookies"""
from fastapi import APIRouter
from fastapi import Path
from fastapi import Query
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import RedirectResponse

from httpbinx.constants import ENV_COOKIES

router = APIRouter(tags=['Cookies'])


@router.get(
    '/cookies',
    summary='Returns cookie data.',
    response_description='Set cookies.',
    response_class=JSONResponse,

)
async def cookies(
        *,
        show_env: bool = Query(
            default=False,
            title='Show Environment variable?',
            include_in_schema=False
        ),
        request: Request
):
    resp = JSONResponse(content={'cookies': request.cookies})
    if not show_env:
        for key in ENV_COOKIES:
            resp.delete_cookie(key)
    return resp


@router.get(
    '/cookies/set',
    summary='Sets cookie(s) as provided by the query string '
            'and redirects to cookie list.',
    response_description='Redirect to cookie list',
    response_class=RedirectResponse
)
async def set_cookies(request: Request):
    params = request.query_params.items()
    resp = RedirectResponse(request.url_for(cookies.__name__))
    for k, v in params:
        # TODO secure=True
        resp.set_cookie(key=k, value=v)
    return resp


@router.get(
    '/cookies/set/{name}/{value}',
    summary='Sets a cookie and redirects to cookie list.',
    response_description='Set cookies and redirects to cookie list.',
    response_class=RedirectResponse,
)
async def set_cookie(
        *,
        name: str = Path(..., description='Cookie Name'),
        value: str = Path(..., description='Cookie Value'),
        request: Request
):
    resp = RedirectResponse(request.url_for(cookies.__name__))
    # TODO secure=True
    resp.set_cookie(key=name, value=value)
    return resp


@router.get(
    '/cookies/delete',
    summary='Deletes cookie(s) as provided by the query string '
            'and redirects to cookie list.',
    response_description='Redirect to cookie list',
    response_class=RedirectResponse
)
async def delete_cookies(request: Request):
    keys = request.query_params.keys()
    resp = RedirectResponse(request.url_for(cookies.__name__))
    for key in keys:
        resp.delete_cookie(key=key)
    return resp
