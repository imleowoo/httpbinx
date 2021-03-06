# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import Path
from starlette.responses import PlainTextResponse
from starlette.responses import Response

from httpbin.helpers import status_code_response
from httpbin.helpers import weighted_choice

router = APIRouter()


@router.api_route(
    '/status/{codes}',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE'],
    description='Return status code or random status code '
                'if more than one are given',
    response_description='TODO'
)
async def status_code(
        *,
        codes: str = Path(
            ...,
            description='a status code or status codes with weight',
            example='200:3,400:1'
        ),
) -> Response:
    invalid_status_code_desc = 'Invalid status code'
    # Only one status code
    if ',' not in codes:
        try:
            code = int(codes)
        except ValueError:
            return PlainTextResponse(
                invalid_status_code_desc,
                status_code=400
            )
        return status_code_response(code)
    # Multiple status codes
    choices = []
    for choice in codes.split(','):
        if ':' not in choice:
            code = choice
            weight = 1  # default weight
        else:
            code, weight = choice.split(':')
        try:
            choices.append((int(code), float(weight)))
        except ValueError:
            return PlainTextResponse(
                invalid_status_code_desc,
                status_code=400
            )
    code = weighted_choice(choices)
    return status_code_response(code)
