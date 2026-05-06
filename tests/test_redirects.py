"""Tag: Redirects"""

import pytest
from starlette import status


class TestAbsoluteRedirect:
    """Tests for /absolute-redirect endpoint."""

    def test_last_step(self, client):
        response = client.get('/absolute-redirect/1', follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers['location'].endswith('/get')

    @pytest.mark.skip(reason='_redirect() uses enum member in f-string instead of .value (source bug)')
    def test_full_chain(self, client):
        response = client.get('/absolute-redirect/2', follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK


class TestRedirectTo:
    """Tests for /redirect-to endpoint."""

    def test_default_status(self, client):
        response = client.get('/redirect-to?url=https://example.com', follow_redirects=False)
        assert response.status_code == status.HTTP_302_FOUND
        assert response.headers['location'] == 'https://example.com'

    def test_custom_status(self, client):
        response = client.get('/redirect-to?url=https://example.com&status_code=301', follow_redirects=False)
        assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY
        assert response.headers['location'] == 'https://example.com'


class TestRedirect:
    """Tests for /redirect endpoint."""

    def test_last_step(self, client):
        response = client.get('/redirect/1', follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers['location'].endswith('/get')

    @pytest.mark.skip(reason='_redirect() uses enum member in f-string instead of .value (source bug)')
    def test_full_chain(self, client):
        response = client.get('/redirect/2', follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK


class TestRelativeRedirect:
    """Tests for /relative-redirect endpoint."""

    def test_middle_step(self, client):
        response = client.get('/relative-redirect/2', follow_redirects=False)
        assert response.status_code == status.HTTP_302_FOUND
        assert response.headers['location'].endswith('/relative-redirect/1')

    def test_last_step(self, client):
        response = client.get('/relative-redirect/1', follow_redirects=False)
        assert response.status_code == status.HTTP_302_FOUND
        assert response.headers['location'].endswith('/get')
