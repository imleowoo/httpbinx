# -*- coding: utf-8 -*-
from fastapi import APIRouter

from httpbin.routers import httpmethods

router = APIRouter()
router.include_router(httpmethods.router, tags=['HTTP Methods'])
