# -*- coding: utf-8 -*-
import json
from enum import Enum
from functools import lru_cache
from typing import AnyStr, Dict, Union

from pydantic import AnyHttpUrl, BaseModel, Field
from starlette.requests import Request


class HTTPMethod(str, Enum):
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
    args: Dict = Field(default_factory=dict, title='Request Args')
    headers: Dict = Field(default_factory=dict, title='Request Headers')
    origin: AnyStr = Field('', title="Client's IP")
    form: Dict = Field(default_factory=dict, title='Request Form')
    data: Union[str, bytes] = Field(b'', title='Request Data')
    files: Dict = Field(default_factory=dict, title='Upload Files')
    json_data: AnyStr = Field('', alias='json', title='Content-Type: application/json', description='serialized')
    method: HTTPMethod = Field(HTTPMethod.get, title='HTTP Request Method')
    extras: Dict = Field(default_factory=dict, title='The Other Information')

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
    def headers(self):
        """request headers."""
        # TODO CaseInsensitiveDict
        return dict(self.request.headers)

    @property
    def client_host(self) -> str:
        """request client host."""
        client = self.request.client
        if client is None:
            return ''
        return client.host

    @property
    async def data(self):
        """request data"""
        return await self.request.body()

    @property
    async def form(self):
        """request form-data"""
        return await self.request.form()

    @property
    async def json(self):
        """request json"""
        try:
            return await self.request.json()
        except json.decoder.JSONDecodeError:
            pass

    @property
    async def files(self):
        """TODO request files."""
        return {}

    @property
    def user_agent(self) -> str:
        """request headers User-Agent"""
        return self.request.headers.get('User-Agent')

    async def request_info(self) -> RequestInfo:
        """fastapi object `Request` to model `RequestInfo`"""
        return RequestInfo(
            url=self.url,
            args=self.args,
            headers=self.headers,
            origin=self.client_host,
            data=await self.data,
            form=await self.form,
            files=await self.files,
            json=json.dumps(await self.json),
            method=self.method,
        )
