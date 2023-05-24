# -*- coding: utf-8 -*-
from fastapi import APIRouter
from starlette.requests import Request

from httpbinx.helpers import to_request_info
from httpbinx.schemas import RequestInfo

router = APIRouter(tags=['Anything'])


@router.api_route(
    '/anything',  # TODO path regex
    response_model=RequestInfo,
    summary='Returns anything passed in request data.',
    response_description='Anything passed in request',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE']
)
async def anything(request: Request):
    return await to_request_info(request)
