# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient

from httpbinx import app

client = TestClient(app)


def test_get():
    response = client.get('/get')
    assert response.status_code == 200
    assert response.json()['origin'] == 'testclient'
