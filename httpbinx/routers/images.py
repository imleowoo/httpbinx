# -*- coding: utf-8 -*-
"""Images"""
from os import path

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.status import HTTP_406_NOT_ACCEPTABLE

from httpbinx.helpers import status_code_response


class ImageResponse(FileResponse):
    """set response headers Content-Type: image/* """
    media_type = 'image/*'


images_path = path.join('static', 'images')

router = APIRouter(
    tags=['Images'],
    default_response_class=ImageResponse
)


@router.get(
    '/image',
    response_class=ImageResponse,
    summary='Returns a simple image of the type suggest by to '
            'Accept header.',
    response_description='An image.'
)
async def image(request: Request):
    accept = request.headers.get('accept')
    if not accept:
        # Default media type to png
        return await image_png()
    accept = accept.lower()
    if 'image/webp' in accept:
        return await image_webp()
    elif 'image/svg+xml' in accept:
        return await image_svg()
    elif 'image/jpeg' in accept:
        return await image_jpeg()
    elif 'image/png' in accept or 'image/*' in accept:
        return await image_png()
    else:
        return status_code_response(HTTP_406_NOT_ACCEPTABLE)


@router.get(
    '/image/png',
    response_class=ImageResponse,
    summary='Returns a simple PNG image.',
    response_description='A PNG image.'
)
async def image_png():
    return ImageResponse(path=path.join(images_path, 'pig_icon.png'))


@router.get(
    '/image/jpeg',
    response_class=ImageResponse,
    summary='Returns a simple JPEG image.',
    response_description='A JPEG image.'
)
async def image_jpeg():
    return ImageResponse(path=path.join(images_path, 'jackal.jpg'))


@router.get(
    '/image/webp',
    response_class=ImageResponse,
    summary='Returns a simple WEBP image.',
    response_description='A WEBP image.'
)
async def image_webp():
    return ImageResponse(path=path.join(images_path, 'wolf_1.webp'))


@router.get(
    '/image/svg',
    response_class=ImageResponse,
    summary='Returns a simple SVG image.',
    response_description='An SVG image.'
)
async def image_svg():
    return ImageResponse(path=path.join(images_path, 'svg_logo.svg'))
