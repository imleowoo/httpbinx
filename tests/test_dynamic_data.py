# -*- coding: utf-8 -*-
"""
Tag: Dynamic Data
"""
from base64 import b64encode
import time
import uuid

from fastapi.testclient import TestClient
from starlette import status

from httpbinx import app

client = TestClient(app)


def test_base64():
    quote = 'Hello, HTTPBINX!'
    b64 = b64encode(quote.encode())
    response = client.get(f'/base64/{b64.decode()}')
    assert response.text == quote


def test_bytes():
    n = 2 ** 10
    response = client.get(f'/bytes/{n}')
    size = 0
    for con in response.iter_bytes():
        size += len(con)
    assert size == n

    # Initialize the random number generator
    seed = 1
    response = client.get(f'/bytes/{n}?seed={seed}')
    size = 0
    for con in response.iter_bytes():
        size += len(con)
    assert size == n

    # Retrieve large bytes.
    n = 2 ** 10 * 1000
    response = client.get(f'/bytes/{n}')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delay():
    delay = 5
    start = time.time()
    response = client.get(f'/delay/{delay}')
    assert response.status_code == status.HTTP_200_OK
    assert time.time() - start > delay


def test_drip(): pass


def test_links(): pass


def test_range(): pass


def test_stream_bytes(): pass


def test_uuid():
    response = client.get('/uuid')
    assert response.status_code == status.HTTP_200_OK
    string = response.json()['uuid']
    uuid.UUID(string)
