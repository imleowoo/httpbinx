# -*- coding: utf-8 -*-
from fastapi import APIRouter

from httpbin.routers import httpmethods
from httpbin.routers.inspection import request_inspection
from httpbin.routers import dynamicdata

router = APIRouter()
router.include_router(httpmethods.router, tags=['HTTP Methods'])
router.include_router(request_inspection.router, tags=['Request Inspection'])
router.include_router(dynamicdata.router, tags=['Dynamic Data'])
