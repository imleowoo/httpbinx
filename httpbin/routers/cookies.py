# -*- coding: utf-8 -*-
"""Cookies"""
from fastapi import APIRouter
from starlette.requests import Request

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
    response_model=RequestDictModel,
    description='Sets cookie(s) as provided by the query string '
                'and redirects to cookie list.',
    response_description='Redirect to cookie list'
)
async def set_cookies(request: Request):
    pass


@router.get('/cookies/set/{name}/{value}')
async def set_cookie(name: str, value: str):
    """Sets a cookie and redirects to cookie list."""
    pass


@router.route('/cookies/delete')
async def delete_cookies():
    """Deletes cookie(s) as provided
    by the query string and redirects to cookie list."""
    pass
