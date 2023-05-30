# -*- coding: utf-8 -*-
"""
Tag: Response Formats
"""
from fastapi.testclient import TestClient
from starlette import status

from httpbinx import app

client = TestClient(app)


def test_brotli():
    response = client.get('/brotli')
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-encoding'] == 'br'


def test_deflate():
    response = client.get('/deflate')
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-encoding'] == 'deflate'


def test_gzip():
    response = client.get('/gzip')
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-encoding'] == 'gzip'


def test_deny():
    response = client.get('/deny')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "YOU SHOULDN'T BE HERE" in response.text


def test_encoding_utf8(): pass


def test_html(): pass


def test_robot(): pass


def test_xml(): pass
