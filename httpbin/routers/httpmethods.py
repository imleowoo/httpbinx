# -*- coding: utf-8 -*-
from fastapi import APIRouter
from starlette.requests import Request

from httpbin.schemas import RequestDictResponseModel

router = APIRouter()


@router.delete('/delete', response_model=RequestDictResponseModel)
async def delete(request: Request):
    pass
