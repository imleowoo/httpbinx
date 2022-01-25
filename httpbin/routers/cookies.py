# -*- coding: utf-8 -*-
"""Cookies"""
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse

from httpbin.constants import ENV_COOKIES
from httpbin.helpers import request_attrs_response
from httpbin.schemas import RequestDictModel

router = APIRouter()


@router.get(
    '/cookies',
    response_model=RequestDictModel,
    description='Returns cookie data.',
    response_description='Set cookies.'
)
async def cookies(
        *,
        show_env: bool = False,
        request: Request
):
    resp = request_attrs_response(
        request,
        keys=('cookies',)
    )
    if show_env:
        for key in ENV_COOKIES:
            resp.delete_cookie(key)
    return resp


@router.get(
    '/cookies/set',
    description='Sets cookie(s) as provided by the query string '
                'and redirects to cookie list.',
    response_description='Redirect to cookie list',
    response_class=RedirectResponse
)
async def set_cookies(request: Request):
    params = request.query_params.items()
    resp = RedirectResponse(request.url_for('cookies'))
    for k, v in params:
        # TODO secure=True
        resp.set_cookie(key=k, value=v)
    return resp


@router.get(
    '/cookies/set/{name}/{value}',
    description='Sets a cookie and redirects to cookie list.',
    response_description='Set cookies and redirects to cookie list.',
    response_class=RedirectResponse
)
async def set_cookie(
        name: str,
        value: str,
        request: Request
):
    resp = RedirectResponse(request.url_for('cookies'))
    # TODO secure=True
    resp.set_cookie(key=name, value=value)


@router.get(
    '/cookies/delete',
    description='Deletes cookie(s) as provided by the query string '
                'and redirects to cookie list.',
    response_description='Redirect to cookie list',
    response_class=RedirectResponse
)
async def delete_cookies(request: Request):
    keys = request.query_params.keys()
    resp = RedirectResponse(request.url_for('cookies'))
    for key in keys:
        resp.delete_cookie(key=key)
    return resp
