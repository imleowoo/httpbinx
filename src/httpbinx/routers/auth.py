"""Auth"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(
    tags=['Auth'],
)
security = HTTPBasic()


@router.get(
    '/basic-auth/{user}/{password}',
    summary='Prompts the user for authorization using HTTP Basic Auth.',
    response_description='TODO',
)
async def basic_auth(user: str, password: str, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if not (credentials and credentials.username == user and credentials.password == password):
        raise HTTPException(status_code=401, headers={'WWW-Authenticate': 'Basic'})

    return {'authenticated': True, 'user': user}
