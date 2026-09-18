from email.utils import parsedate_to_datetime

import pytest


def test_cache_emits_validators_without_mutating_request_headers(client):
    response = client.get('/cache?name=value', headers={'X-Probe': 'preserved'})
    assert response.status_code == 200
    assert parsedate_to_datetime(response.headers['Last-Modified'])
    assert response.headers['ETag']
    body = response.json()
    assert body['args'] == {'name': 'value'}
    assert body['headers']['x-probe'] == 'preserved'
    assert 'Last-Modified' not in body['headers']
    assert 'ETag' not in body['headers']
    for header in ['If-Modified-Since', 'If-None-Match']:
        conditional = client.get('/cache', headers={header: response.headers['ETag']})
        assert conditional.status_code == 304
        assert conditional.content == b''


@pytest.mark.parametrize('seconds', [0, 60, 3600])
def test_cache_control_is_an_http_header(client, seconds):
    response = client.get(f'/cache/{seconds}', headers={'Cache-Control': 'no-cache'})
    assert response.status_code == 200
    assert response.headers['Cache-Control'] == f'public, max-age={seconds}'
    assert response.json()['headers']['cache-control'] == 'no-cache'
    assert 'Cache-Control' not in response.json()['headers']


@pytest.mark.parametrize(
    ('headers', 'status_code'),
    [
        ({}, 200),
        ({'If-None-Match': 'other'}, 200),
        ({'If-Match': 'probe'}, 200),
        ({'If-None-Match': 'probe'}, 304),
        ({'If-None-Match': '*'}, 304),
        ({'If-Match': 'other'}, 412),
    ],
)
def test_etag_response_header_and_existing_conditions(client, headers, status_code):
    response = client.get('/etag/probe', headers=headers)
    assert response.status_code == status_code
    if status_code in [200, 304]:
        assert response.headers['ETag'] == 'probe'
    if status_code == 200:
        assert 'ETag' not in response.json()['headers']
    elif status_code == 304:
        assert response.content == b''
