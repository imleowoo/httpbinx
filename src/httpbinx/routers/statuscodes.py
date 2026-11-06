from math import isfinite

from fastapi import APIRouter, Path
from starlette.responses import PlainTextResponse, Response

from httpbinx.helpers import status_code_response, weighted_choice

router = APIRouter(tags=['Status codes'])


@router.api_route(
    '/status/{codes}',
    methods=['GET'],
    summary='Return status code or random status code if more than one are given',
    response_description='Response corresponding to different HTTP status codes.',
)
async def status_code(
    *,
    codes: str = Path(
        ...,
        description='a status code or status codes with finite positive weights',
        # examples=['200:3,400:1'],
        openapi_examples={'sample': {'value': '200:3,400:1'}},
    ),
) -> Response:
    invalid_status_code_desc = 'Invalid status code'
    # Only one status code
    if ',' not in codes:
        try:
            code = int(codes)
        except ValueError:
            return PlainTextResponse(invalid_status_code_desc, status_code=400)
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
            parsed_weight = float(weight)
            if not isfinite(parsed_weight) or parsed_weight <= 0:
                return PlainTextResponse(invalid_status_code_desc, status_code=400)
            choices.append((int(code), parsed_weight))
        except ValueError:
            return PlainTextResponse(invalid_status_code_desc, status_code=400)
    if not isfinite(sum(weight for _, weight in choices)):
        return PlainTextResponse(invalid_status_code_desc, status_code=400)
    code = weighted_choice(choices)
    return status_code_response(code)
