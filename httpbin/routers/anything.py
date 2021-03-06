# -*- coding: utf-8 -*-
from fastapi import APIRouter
from starlette.requests import Request

from httpbin.helpers import request_attrs_response
from httpbin.schemas import RequestDictModel

router = APIRouter()


@router.api_route(
    '/anything',    # TODO path regex
    response_model=RequestDictModel,
    description='Returns anything passed in request data.',
    response_description='Anything passed in request',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE']
)
async def anything(request: Request):
    return request_attrs_response(
        request,
        keys=(
            'url', 'args', 'form', 'data', 'origin',
            'headers', 'files', 'json', 'method'
        )
    )
