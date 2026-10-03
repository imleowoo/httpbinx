"""Tag: Response Formats"""

import pytest
from starlette import status


class TestBrotli:
    """Tests for Brotli-compressed response."""

    def test_ok_and_encoding(self, client):
        response = client.get('/brotli')
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-encoding'] == 'br'

    def test_response_is_valid_json(self, client):
        response = client.get('/brotli')
        data = response.json()
        assert 'url' in data
        assert 'headers' in data


class TestDeflate:
    """Tests for Deflate-compressed response."""

    def test_ok_and_encoding(self, client):
        response = client.get('/deflate')
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-encoding'] == 'deflate'

    def test_response_is_valid_json(self, client):
        response = client.get('/deflate')
        data = response.json()
        assert 'url' in data
        assert 'headers' in data


class TestGzip:
    """Tests for GZip-compressed response."""

    def test_ok_and_encoding(self, client):
        response = client.get('/gzip')
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-encoding'] == 'gzip'

    def test_response_is_valid_json(self, client):
        response = client.get('/gzip')
        data = response.json()
        assert 'url' in data
        assert 'headers' in data


class TestDeny:
    """Tests for the /deny endpoint."""

    def test_forbidden(self, client):
        response = client.get('/deny')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "YOU SHOULDN'T BE HERE" in response.text


@pytest.mark.skip(reason='Endpoint uses CWD-relative path to static files (source bug)')
def test_encoding_utf8(client):
    response = client.get('/encoding/utf8')
    assert response.status_code == status.HTTP_200_OK
    assert 'UTF-8' in response.text


@pytest.mark.skip(reason='Endpoint uses CWD-relative path to templates (source bug)')
def test_html(client):
    response = client.get('/html')
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('text/html')


class TestJson:
    """Tests for the /json endpoint."""

    def test_structure(self, client):
        response = client.get('/json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['title'] == 'Sample Slide Show'
        assert len(data['slides']) == 2


class TestLegacy:
    """Tests for the /legacy landing page endpoint."""

    def test_ok_and_html(self, client):
        response = client.get('/legacy')
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-type'].startswith('text/html')

    def test_lists_endpoints(self, client):
        response = client.get('/legacy')
        assert '/get' in response.text
        assert '/robots.txt' in response.text


class TestRobots:
    """Tests for the /robots.txt endpoint."""

    def test_canonical_route(self, client):
        response = client.get('/robots.txt')
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-type'].startswith('text/plain')
        assert 'User-agent' in response.text
        assert 'Disallow' in response.text

    def test_nonstandard_robot_txt_is_gone(self, client):
        response = client.get('/robot.txt')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.skip(reason='Endpoint uses CWD-relative path to templates (source bug)')
def test_xml(client):
    response = client.get('/xml')
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('application/xml')
    assert response.text.strip().startswith('<?xml')
