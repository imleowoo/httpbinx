"""Tag: Status Codes"""

from urllib import parse

from starlette import status


def test_status_codes_all_methods(client):
    for name in [c for c in dir(status) if c.startswith('HTTP') and c not in status.__deprecated__]:
        target_code = getattr(status, name)
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE']:
            response = client.request(method=method, url=f'/status/{target_code}')
            assert response.status_code in [target_code, status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED]


def test_status_code_weighted_random(client):
    code_weight = {status.HTTP_200_OK: 2, status.HTTP_302_FOUND: 1, status.HTTP_400_BAD_REQUEST: 1}
    weight_string = ','.join(f'{code}:{weight}' for code, weight in code_weight.items())
    response = client.get(f'/status/{parse.quote(weight_string)}')
    assert response.status_code in code_weight


def test_status_code_invalid_weight(client):
    response = client.get('/status/invalid_code_and_weight')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.text == 'Invalid status code'


def test_status_code_non_numeric(client):
    response = client.get('/status/abc')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.text == 'Invalid status code'


def test_status_code_single(client):
    response = client.get('/status/201')
    assert response.status_code == status.HTTP_201_CREATED
