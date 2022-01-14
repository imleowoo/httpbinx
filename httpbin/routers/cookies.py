# -*- coding: utf-8 -*-
"""Cookies"""
from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()


@router.get('/cookies')
async def cookies(request: Request):
    """Return cookie data"""
    pass


@router.get('/cookies/set')
async def set_cookies():
    """Sets cookie(s) as provided
    by the query string and redirects to cookie list."""
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
