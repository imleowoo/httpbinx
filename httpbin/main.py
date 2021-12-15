# -*- coding: utf-8 -*-
from fastapi import FastAPI

from httpbin.routers import router

app = FastAPI(
    title='fastapi-httpbin'
)

app.include_router(router=router, prefix='/api')
