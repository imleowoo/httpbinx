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

    json_data = form_data = {
        'name': 'Albert Einstein',
        'age': str(datetime.now().year - 1879)
    }
    # application/x-www-form-urlencoded
    response = client.post('/post', data=form_data.copy())
    assert response.json()['form'] == form_data

    # application/json
    response = client.post('/post', json=json_data.copy())
    assert response.json()['json'] == json_data
