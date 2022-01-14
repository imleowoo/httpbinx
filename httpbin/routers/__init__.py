# -*- coding: utf-8 -*-
from fastapi import APIRouter

from httpbin.routers import anything
from httpbin.routers import auth
from httpbin.routers import dynamicdata
from httpbin.routers import httpmethods
from httpbin.routers import redirects
from httpbin.routers import responseformats
from httpbin.routers import statuscodes
from httpbin.routers.inspection import request_inspection
from httpbin.routers.inspection import response_inspection

router = APIRouter()
router.include_router(httpmethods.router, tags=['HTTP Methods'])
router.include_router(request_inspection.router, tags=['Request inspection'])
router.include_router(response_inspection.router, tags=['Response inspection'])
router.include_router(dynamicdata.router, tags=['Dynamic data'])
router.include_router(responseformats.router, tags=['Response formats'])
router.include_router(redirects.router, tags=['Redirects'])
router.include_router(anything.router, tags=['Anything'])
router.include_router(auth.router, tags=['Auth'])
router.include_router(statuscodes.router, tags=['Status codes'])
router.include_router(anything.router, tags=['Anything'])
