"""Tag: HTTP Methods"""

import json
from datetime import datetime

from starlette import status


class TestGet:
    """Tests for GET /get."""

    def test_status(self, client):
        response = client.get('/get')
        assert response.status_code == status.HTTP_200_OK

    def test_response_fields(self, client):
        response = client.get('/get')
        data = response.json()
        assert data['url'].endswith('/get')
        assert 'headers' in data
        assert 'args' in data
        assert 'origin' in data

    def test_with_query_params(self, client):
        response = client.get('/get?foo=bar&baz=1')
        assert response.json()['args'] == {'foo': 'bar', 'baz': '1'}


class TestPost:
    """Tests for POST /post."""

    def test_string_body(self, client):
        content = b'httpbinx'
        response = client.post('/post', content=content)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data'] == content.decode()

    def test_form_data(self, client):
        data = {'name': 'Albert Einstein', 'age': str(datetime.now().year - 1879)}
        response = client.post('/post', data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['form'] == data

    def test_json(self, client):
        data = {'name': 'Albert Einstein', 'age': str(datetime.now().year - 1879)}
        response = client.post('/post', json=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['json'] == json.dumps(data)


class TestPut:
    """Tests for PUT /put."""

    def test_basic(self, client):
        response = client.put('/put', json={'key': 'value'})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['method'] == 'PUT'

    def test_with_body(self, client):
        response = client.put('/put', json={'key': 'value'})
        assert response.json()['json'] == json.dumps({'key': 'value'})


class TestDelete:
    """Tests for DELETE /delete."""

    def test_basic(self, client):
        response = client.delete('/delete')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['method'] == 'DELETE'


class TestPatch:
    """Tests for PATCH /patch."""

    def test_basic(self, client):
        response = client.patch('/patch', json={'patch': 'data'})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['method'] == 'PATCH'

    def test_with_body(self, client):
        response = client.patch('/patch', json={'patch': 'data'})
        assert response.json()['json'] == json.dumps({'patch': 'data'})
