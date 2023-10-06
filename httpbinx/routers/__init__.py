# -*- coding: utf-8 -*-

__all__ = ['router']

from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from httpbinx.routers import anything
from httpbinx.routers import auth
from httpbinx.routers import cookies
from httpbinx.routers import dynamicdata
from httpbinx.routers import httpmethods
from httpbinx.routers import images
from httpbinx.routers import redirects
from httpbinx.routers import responseformats
from httpbinx.routers import statuscodes
from httpbinx.routers.inspection import request_inspection
from httpbinx.routers.inspection import response_inspection

router = APIRouter()


@router.get(
    '/favicon.ico',
    summary='Returns a favicon.ico.',
    include_in_schema=False
)
async def favicon():
    return RedirectResponse(
        url='/static/favicon.png',
        status_code=status.HTTP_301_MOVED_PERMANENTLY
    )


router.include_router(httpmethods.router)
router.include_router(request_inspection.router)
router.include_router(response_inspection.router, include_in_schema=False)
router.include_router(dynamicdata.router)
router.include_router(responseformats.router)
router.include_router(redirects.router)
router.include_router(anything.router)
router.include_router(auth.router, include_in_schema=False)
router.include_router(statuscodes.router)
router.include_router(images.router)
router.include_router(cookies.router)
