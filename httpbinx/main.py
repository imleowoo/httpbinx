from os import path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from httpbinx.meta import tags_metadata
from httpbinx.routers import router

app = FastAPI(
    title='httpbinx',
    description='HTTP Request & Response Service, '
                'written in Python + FastAPI.',
    docs_url='/',  # swagger docs page url
    swagger_ui_parameters={'docExpansion': 'none'},
    openapi_tags=tags_metadata
)

app.mount(
    '/static',
    StaticFiles(directory=path.join(path.dirname(__file__), 'static')),
    name='static'
)

# app.openapi_tags = []
app.include_router(router=router)
