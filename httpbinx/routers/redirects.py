# -*- coding: utf-8 -*-
from enum import Enum

from fastapi import APIRouter
from fastapi import Path
from fastapi import Query
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.responses import Response

router = APIRouter(tags=['Redirects'])


class RedirectTypes(str, Enum):
    DEFAULT = 'redirect'
    ABSOLUTE = 'absolute_redirect'
    RELATIVE = 'relative_redirect'


@router.get(
    '/absolute-redirect/{n}',
    summary='Absolutely 302 Redirects n times.',
    response_description='A redirection.',
    response_class=RedirectResponse,
)
async def absolute_redirect_n_times(
        *,
        n: int = Path(..., title='Redirects n times.', gt=0, le=10),
        request: Request
):
    if n == 1:
        return RedirectResponse(request.url_for('get'))
    return _redirect(request, type_=RedirectTypes.ABSOLUTE, n=n)


@router.api_route(
    '/redirect-to',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE'],
    summary='302/3XX Redirects to the given URL.',
    response_description='A redirection.',
    response_class=Response
)
async def redirect_to(
        *,
        url: str = Query(..., title='Redirect to URL'),
        status_code: int = Query(
            status.HTTP_302_FOUND,
            title='status code',
            ge=status.HTTP_300_MULTIPLE_CHOICES,
            lt=status.HTTP_400_BAD_REQUEST,
        ),
):
    resp = Response(status_code=status_code)
    resp.headers['Location'] = url
    return resp


@router.get(
    '/redirect/{n}',
    summary='302 Redirects n times.',
    response_description='A redirection.'
)
async def redirect_n_times(
        *,
        n: int = Path(..., title='Redirects n times.', gt=0, le=10),
        is_absolute: bool = Query(
            False,
            alias='absolute',
            title='is an absolute redirection？'
        ),
        request: Request
):
    if n == 1:
        return RedirectResponse(request.url_for('get'))
    if is_absolute:
        return _redirect(request, type_=RedirectTypes.ABSOLUTE, n=n)
    else:
        return _redirect(request, type_=RedirectTypes.RELATIVE, n=n)


@router.get(
    '/relative-redirect/{n}',
    summary='Relatively 302 Redirects n times.',
    response_description='A redirection.'
)
async def relative_redirect_n_times(
        *,
        n: int = Path(..., title='Redirects n times.', gt=0, le=10),
        request: Request
):
    resp = Response(status_code=status.HTTP_302_FOUND)
    if n == 1:
        resp.headers['Location'] = str(request.url_for('get'))
        return resp
    redirect_name = relative_redirect_n_times.__name__
    resp.headers['Location'] = str(request.url_for(redirect_name, n=n - 1))
    return resp


def _redirect(request: Request, type_: RedirectTypes, n: int):
    # TODO external
    # "absolute_redirect" and "relative_redirect" options are not effective.
    func_prefix = f'{type_}_n_times'
    return RedirectResponse(request.url_for(func_prefix, n=n - 1))
