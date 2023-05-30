# -*- coding: utf-8 -*-
"""
Tag: Anything
"""
from fastapi.testclient import TestClient
from starlette import status

from httpbinx import app

client = TestClient(app)


def test_anything():
    for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE']:
        response = client.request(method=method, url='/anything')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['method'] == method
