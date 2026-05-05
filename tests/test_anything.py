"""Tag: Anything"""

from starlette import status


class TestAnything:
    """Tests for the /anything endpoint."""

    def test_all_methods(self, client):
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE']:
            response = client.request(method=method, url='/anything')
            assert response.status_code == status.HTTP_200_OK
            assert response.json()['method'] == method

    def test_with_body(self, client):
        response = client.post('/anything', json={'hello': 'world'})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['method'] == 'POST'
        assert '"hello"' in data['json']

    def test_with_query_params(self, client):
        response = client.get('/anything?foo=bar&baz=1')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['args'] == {'foo': 'bar', 'baz': '1'}

    def test_with_headers(self, client):
        response = client.get('/anything', headers={'X-Custom': 'test-value'})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['headers']['x-custom'] == 'test-value'


class TestBombs:
    """Tests for the /bombs endpoint."""

    def test_brotli(self, client):
        response = client.get('/bombs/brotli')
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-encoding'] == 'br'

    def test_gzip(self, client):
        response = client.get('/bombs/gzip')
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-encoding'] == 'gzip'
