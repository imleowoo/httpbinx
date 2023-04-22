# -*- coding: utf-8 -*-
"""Auth"""
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

router = APIRouter()


@router.get(
    '/basic-auth/{user}/{password}',
    summary='Prompts the user for authorization using HTTP Basic Auth.',
    response_description='TODO'
)
async def basic_auth(
        user: str,
        password: str,
        request: Request
) -> JSONResponse:
    pass
