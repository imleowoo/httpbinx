# -*- coding: utf-8 -*-
"""Auth"""
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

router = APIRouter(tags=['Auth'],)
security = HTTPBasic()


@router.get(
    '/basic-auth/{user}/{password}',
    summary='Prompts the user for authorization using HTTP Basic Auth.',
    response_description='TODO'
)
async def basic_auth(
        user: str,
        password: str,
        credentials: HTTPBasicCredentials = security
):
    if not (credentials and credentials.username == user and credentials.password == password):
        raise HTTPException(status_code=401)

    return {'authenticated': True, 'user': user}
