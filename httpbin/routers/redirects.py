# -*- coding: utf-8 -*-
from fastapi import APIRouter

router = APIRouter()


@router.get('/absolute-redirect/{n}')
async def absolute_redirect_n_times(n: int):
    """Absolutely 302 Redirects n times."""
    pass


@router.api_route(
    '/redirect-to',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE']
)
async def redirect_to():
    """302/3XX Redirects to the given URL."""
    pass


@router.get('/redirect/{n}')
async def redirect_n_times():
    """302 Redirects n times."""
    pass


@router.get('/relative-redirect/{n}')
async def relative_redirect_n_times(n: int):
    """Relatively 302 Redirects n times."""
    pass
