# -*- coding: utf-8 -*-
"""
Tag: Dynamic Data
"""
from fastapi.testclient import TestClient

from httpbinx import app

client = TestClient(app)


def test_base64():
    from base64 import b64encode
    quote = 'Hello, HTTPBINX!'
    b64 = b64encode(quote.encode())
    response = client.get(f'/base64/{b64.decode()}')
    assert response.text == quote


def test_bytes(): pass


def test_delay(): pass


def test_drip(): pass


def test_links(): pass


def test_range(): pass


def test_stream_bytes(): pass


def test_uuid(): pass
