"""HTTP Methods."""
from fastapi import APIRouter
from starlette.requests import Request

from httpbinx.helpers import to_request_info
from httpbinx.schemas import RequestInfo

router = APIRouter(tags=['HTTP Methods'])


async def method_handler(request: Request) -> RequestInfo:
    """Handle request and return request info."""
    return await to_request_info(request)


router.get(
    '/get',
    response_model=RequestInfo,
    response_model_include={'url', 'args', 'headers', 'origin'},
    summary="The request's query parameters.",
    response_description="The request's query parameters."
)(method_handler)

router.post(
    '/post',
    response_model=RequestInfo,
    summary="The request's POST parameters.",
    response_description="The request's POST parameters."
)(method_handler)

router.put(
    '/put',
    response_model=RequestInfo,
    summary="The request's PUT parameters.",
    response_description="The request's PUT parameters."
)(method_handler)

router.delete(
    '/delete',
    response_model=RequestInfo,
    summary="The request's DELETE parameters.",
    response_description="The request's DELETE parameters."
)(method_handler)

router.patch(
    '/patch',
    response_model=RequestInfo,
    summary="The request's PATCH parameters.",
    response_description="The request's PATCH parameters."
)(method_handler)
