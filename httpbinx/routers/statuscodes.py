# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import Path
from starlette.responses import PlainTextResponse
from starlette.responses import Response

from httpbinx.helpers import status_code_response
from httpbinx.helpers import weighted_choice

router = APIRouter(tags=['Status codes'])


@router.api_route(
    '/status/{codes}',
    methods=['GET'],
    summary='Return status code or random status code '
            'if more than one are given',
    response_description='Response corresponding to different HTTP status codes.'
)
async def status_code(
        *,
        codes: str = Path(
            ...,
            description='a status code or status codes with weight',
            # examples=['200:3,400:1'],
            openapi_examples={
                'sample': {'value': '200:3,400:1'}
            }
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
