# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient

from httpbinx import app

client = TestClient(app)


def test_get():
    response = client.get('/get')
    assert response.status_code == 200
    assert response.json()['origin'] == 'testclient'


def test_post():
    from datetime import datetime

    data = {
        'name': 'Albert Einstein',
        'age': str(datetime.now().year - 1879)
    }
    # string or bytes
    str_or_bytes = b'httpbinx'
    response = client.post('/post', content=str_or_bytes)
    target = str_or_bytes.decode() if isinstance(str_or_bytes, bytes) else str_or_bytes
    assert response.json()['data'] == target

    # application/x-www-form-urlencoded
    response = client.post('/post', data=data.copy())
    assert response.json()['form'] == data

    # application/json
    response = client.post('/post', json=data.copy())
    assert response.json()['json'] == data
