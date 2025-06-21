from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from httpbinx.meta import get_tags_metadata
from httpbinx.routers import router

app = FastAPI(
    title='httpbinx',
    description='HTTP Request & Response Service, '
                'written in Python + FastAPI.',
    docs_url='/',  # swagger docs page url
    swagger_ui_parameters={'docExpansion': 'none'},
    openapi_tags=get_tags_metadata()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],

)

# mount static files
static_dir = Path(__file__).parent / 'static'
app.mount(
    '/static',
    StaticFiles(directory=static_dir),
    name='static'
)

app.include_router(router=router)
