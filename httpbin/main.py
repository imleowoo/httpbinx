# -*- coding: utf-8 -*-
from fastapi import FastAPI

from httpbin.routers import router

app = FastAPI(title='FastAPI-httpbin')

app.include_router(router=router, prefix='/api')
