# -*- coding: utf-8 -*-

__all__ = ['router']

from fastapi import APIRouter

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
router.include_router(httpmethods.router, tags=['HTTP Methods'])
router.include_router(request_inspection.router, tags=['Request inspection'])
router.include_router(response_inspection.router, tags=['Response inspection'],
                      include_in_schema=False)
router.include_router(dynamicdata.router, tags=['Dynamic data'])
router.include_router(responseformats.router, tags=['Response formats'])
router.include_router(redirects.router, tags=['Redirects'])
router.include_router(anything.router, tags=['Anything'])
router.include_router(auth.router, tags=['Auth'], include_in_schema=False)
router.include_router(statuscodes.router, tags=['Status codes'])
router.include_router(anything.router, tags=['Anything'])
router.include_router(images.router, tags=['Images'])
router.include_router(cookies.router, tags=['Cookies'])
