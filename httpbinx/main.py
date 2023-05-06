# -*- coding: utf-8 -*-
from os import path

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from httpbinx.routers import router

app = FastAPI(
    title='httpbinx',
    description='HTTP Request & Response Service, '
                'written in Python + FastAPI.',
    docs_url='/',  # swagger docs page url
    swagger_ui_parameters={'docExpansion': 'none'},
)

app.mount(
    '/static',
    StaticFiles(directory=path.join(path.dirname(__file__), 'static')),
    name='static'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# app.openapi_tags = []
app.include_router(router=router)
