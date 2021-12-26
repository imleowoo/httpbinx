# -*- coding: utf-8 -*-
from fastapi import FastAPI

from httpbin.routers import router

app = FastAPI(
    title='FastAPI-httpbin'
)

# app.add_middleware(
#     AuthenticationMiddleware,
#     backend=AuthenticationBackend()
# )
app.include_router(router=router, prefix='/api')
