# -*- coding: utf-8 -*-
from enum import Enum
from functools import lru_cache
from typing import Optional
from typing import Union

from pydantic import AnyHttpUrl
from pydantic import BaseModel
from pydantic import Field
from starlette.requests import Request


class HTTPMethods(str, Enum):
    """ HTTP request methods

    References:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    get = 'GET'
    head = 'HEAD'
    post = 'POST'
    put = 'PUT'
    delete = 'DELETE'
    connect = 'CONNECT'
    options = 'OPTIONS'
    trace = 'TRACE'
    patch = 'PATCH'


class RequestInfo(BaseModel):
    """Data structure about request dict

    References:
        - AnyHttpUrl vs HttpUrl: https://docs.pydantic.dev/usage/types/#urls
    """

    url: AnyHttpUrl = Field(title='Request URL')
    args: dict = Field(default_factory=dict, title='Request Args')
    form: dict = Field(default_factory=dict, title='Request Form')
    data: str = Field('', title='Request Data')
    headers: dict = Field(default_factory=dict, title='Request Headers')
    origin: str = Field('', title="Client's IP")
    files: dict = Field(default_factory=dict, title='Upload Files')
    json_data: Optional[Union[str, list]] = Field(
        None, alias='json', title='Content-Type: application/json'
    )
    method: HTTPMethods = Field(HTTPMethods.get, title='HTTP Request Method')
    extras: dict = Field(default_factory=dict, title='The Other Information')

    @classmethod
    def get_properties(cls):
        """Get declared property fields"""

        @lru_cache
        def properties():
            return tuple(cls.schema()['properties'].keys())

        return properties()


class RequestAttrs:

    def __init__(self, request: Request):
        self._request = request

    @property
    def request(self):
        """Read only"""
        return self._request

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
        for a key, the result will have a list of values for the key.
        Otherwise it will have the plain value."""
        out = dict()
        for k, v in self.request.query_params.multi_items():
            exist = out.get(k)
            if exist:
                out[k] = exist.append(v) \
                    if isinstance(exist, list) else [exist, v]
            else:
                out[k] = v
        return out

    @property
    def form(self):
        """TODO request form"""
        return dict()

    @property
    def data(self):
        """TODO request data."""
        return ''

    @property
    def headers(self):
        """request headers."""
        # TODO CaseInsensitiveDict
        return dict(self.request.headers)

    @property
    def client_host(self) -> str:
        """request client host."""
        return self.request.client.host

    @property
    def files(self):
        """TODO request files."""
        return ''

    @property
    def json(self):
        """TODO request json."""
        return None

    @property
    def user_agent(self) -> str:
        """request headers User-Agent"""
        return self.request.headers.get('User-Agent')

    @property
    def cookies(self) -> dict:
        """request cookies"""
        return self.request.cookies

    @property
    @lru_cache(maxsize=1)
    def request_info(self) -> RequestInfo:
        """fastapi object `Request` to model `RequestInfo`"""
        return RequestInfo(
            url=self.url,
            args=self.args,
            form=self.form,
            data=self.data,
            headers=self.headers,
            origin=self.client_host,
            files=self.files,
            json_data=self.json,
            method=self.method,
        )
