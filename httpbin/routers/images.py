# -*- coding: utf-8 -*-
"""Images"""

from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()


@router.get('/image')
async def image(request: Request):
    """Returns a simple image of the type suggest by the Accept header."""
    pass


@router.get('/image/png')
async def image_png():
    """Returns a simple PNG image."""
    pass


@router.get('/image/jpeg')
async def image_jpeg():
    """Returns a simple JPEG image."""
    pass


@router.get('/image/webp')
async def image_webp():
    """Returns a simple WEBP image."""
    pass


@router.get('/image/svg')
async def image_svg():
    """Returns a simple SVG image."""
    pass
