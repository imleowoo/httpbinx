from enum import Enum
from functools import lru_cache
from typing import Union

from pydantic import BaseModel, Field
from starlette.requests import Request


class HTTPMethods(str, Enum):
    get = 'GET'
    head = 'HEAD'
    post = 'POST'
    put = 'PUT'
    delete = 'DELETE'
    connect = 'CONNECT'
    options = 'OPTIONS'
    trace = 'TRACE'
    patch = 'PATCH'


class RequestAttrs:

    def __init__(self, request: Request):
        self.request = request

    @property
    def method(self):
        """request http method"""
        return self.request.method

    @property
    def url(self):
        """request url."""
        return str(self.request.url)

    @property
    def args(self):
        """request url args.
        If there are more than one value
        for a key, the result will have a list of values for the key. Otherwise it
        will have the plain value."""
        out = dict()
        for k, v in self.request.query_params.items():
            if k in out:
                # TODO
                pass
        return out

    @property
    def form(self):
        """request form"""
        return dict()

    @property
    def data(self):
        """request data."""
        return ''

    @property
    def headers(self):
        """request headers."""
        # TODO CaseInsensitiveDict
        return dict(self.request.headers)

    @property
    def client_host(self):
        """request client host."""
        return self.request.client.host

    @property
    def files(self):
        """request files."""
        return ''

    @property
    def json(self):
        """request json."""
        return None


class RequestDictModel(BaseModel):
    """Data structure about request dict"""

    url: str = Field(..., title='Request URL')
    args: dict = Field(default_factory=dict, title='Request Args')
    form: dict = Field(default_factory=dict, title='Request Form')
    data: str = Field('', title='Request Data')
    headers: dict = Field(default_factory=dict, title='Request Headers')
    origin: str = Field('', title="Client's IP")
    files: dict = Field(default_factory=dict, title='Upload Files')
    json_data: Union[list, dict] = Field(None, alias='json', title='Content-Type: JSON')
    method: HTTPMethods = Field(..., title='HTTP Request method')

    @classmethod
    def get_properties(cls):
        @lru_cache
        def properties():
            return tuple(cls.schema()['properties'].keys())

        return properties()
