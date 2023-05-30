# -*- coding: utf-8 -*-
"""
Tag: Status Codes
"""
from urllib import parse

from fastapi.testclient import TestClient
from starlette import status

from httpbinx import app

client = TestClient(app)


def test_status_codes():
    # All HTTP Codes
    for name in [c for c in dir(status) if c.startswith('HTTP')]:
        target_code = getattr(status, name)
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE']:
            response = client.request(method=method, url=f'/status/{target_code}')
            assert response.status_code in [
                target_code,
                status.HTTP_200_OK,
                status.HTTP_405_METHOD_NOT_ALLOWED
            ]

    # Random HTTP Codes
    code_weight = {
        status.HTTP_200_OK: 2,
        status.HTTP_302_FOUND: 1,
        status.HTTP_400_BAD_REQUEST: 1
    }
    # like: `200:3,400:1`
    weight_string = ','.join(f'{code}:{weight}' for code, weight in code_weight.items())
    response = client.get(f'/status/{parse.quote(weight_string)}')
    assert response.status_code in code_weight

    # Invalid wight
    invalid_weight_string = 'invalid_code_and_weight'
    response = client.get(f'/status/{parse.quote(invalid_weight_string)}')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.text == 'Invalid status code'
