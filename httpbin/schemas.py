from enum import Enum
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


class RequestAttrs(BaseModel):
    _request: Request

    @property
    def method(self):
        """request http method"""
        return self._request.method

    @property
    def url(self):
        """request url."""
        return self._request.url

    @property
    def args(self):
        """request url args.
        If there are more than one value
        for a key, the result will have a list of values for the key. Otherwise it
        will have the plain value."""
        out = dict()
        for k, v in self._request.query_params:
            if k in out:
                # TODO
                pass
        return out

    @property
    def form(self):
        """request form"""
        return None

    @property
    def data(self):
        """request data."""
        return None

    @property
    def headers(self):
        """request headers."""
        # TODO CaseInsensitiveDict
        return dict(self._request.headers)

    @property
    def client_host(self):
        """request client host."""
        return self._request.client.host

    @property
    def files(self):
        """request files."""
        return None

    @property
    def json_(self):
        """request json."""
        return None


class RequestDictResponseModel(BaseModel):
    """Response data structure about request dict"""

    url: str = Field(..., title='Request URL')
    args: dict = Field(default_factory=dict, title='Request Args')
    form: dict = Field(default_factory=dict, title='Request Form')
    data: str = Field('', title='Request Data')
    headers: dict = Field(default_factory=dict, title='Request Headers')
    origin: str = Field('', title="Client's IP")
    files: dict = Field(default_factory=dict, title='Upload Files')
    json_data: Union[list, dict] = Field(None, alias='json', title='Content-Type: JSON')
    method: HTTPMethods = Field(..., title='HTTP Request method')
