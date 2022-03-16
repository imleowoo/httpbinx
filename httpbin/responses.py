# -*- coding: utf-8 -*-
from starlette.responses import FileResponse
from starlette.responses import Response


class ImageResponse(FileResponse):
    """set response headers Content-Type: image/* """
    media_type = 'image/*'


class OctetStreamResponse(Response):
    """set response headers Content-Type: application/octet-stream"""
    media_type = 'application/octet-stream'
