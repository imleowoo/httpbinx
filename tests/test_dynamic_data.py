"""Tag: Dynamic Data"""

import time
import uuid
from base64 import b64encode

import pytest
from starlette import status


class TestBase64:
    """Tests for the /base64 endpoint."""

    def test_decode(self, client):
        quote = 'Hello, HTTPBINX!'
        b64 = b64encode(quote.encode())
        response = client.get(f'/base64/{b64.decode()}')
        assert response.status_code == status.HTTP_200_OK
        assert response.text == quote

    def test_invalid(self, client):
        response = client.get('/base64/!!!invalid!!!')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Incorrect Base64 data' in response.text


class TestBytes:
    """Tests for the /bytes endpoint."""

    def test_small(self, client):
        n = 2**10
        response = client.get(f'/bytes/{n}')
        size = sum(len(con) for con in response.iter_bytes())
        assert size == n

    def test_with_seed(self, client):
        n = 2**10
        response = client.get(f'/bytes/{n}?seed=1')
        size = sum(len(con) for con in response.iter_bytes())
        assert size == n

    def test_too_large(self, client):
        n = 2**10 * 1000
        response = client.get(f'/bytes/{n}')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


class TestDelay:
    """Tests for the /delay endpoint."""

    def test_minimum_delay(self, client):
        delay = 0.05
        start = time.time()
        response = client.get(f'/delay/{delay}')
        assert response.status_code == status.HTTP_200_OK
        elapsed = time.time() - start
        assert elapsed >= delay


class TestDrip:
    """Tests for the /drip endpoint."""

    def test_basic(self, client):
        response = client.get('/drip?duration=1&numbytes=5&code=200&delay=0.05')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.content) == 5

    def test_respects_duration(self, client):
        duration = 0.2
        start = time.time()
        response = client.get(f'/drip?duration={duration}&numbytes=10&delay=0')
        elapsed = time.time() - start
        assert response.status_code == status.HTTP_200_OK
        assert len(response.content) == 10
        assert elapsed >= duration

    def test_large_numbytes_is_paced(self, client):
        duration = 0.2
        numbytes = 100_000
        start = time.time()
        response = client.get(f'/drip?duration={duration}&numbytes={numbytes}&delay=0')
        elapsed = time.time() - start
        assert response.status_code == status.HTTP_200_OK
        assert len(response.content) == numbytes
        assert elapsed >= duration

    def test_large_numbytes_drips_without_per_byte_sleeps(self, client, monkeypatch):
        import asyncio as asyncio_module
        import types

        from httpbinx.routers import dynamicdata

        delays = []

        async def fake_sleep(delay):
            delays.append(delay)
            await asyncio_module.sleep(0)

        monkeypatch.setattr(dynamicdata, 'asyncio', types.SimpleNamespace(sleep=fake_sleep))

        response = client.get('/drip?duration=1&numbytes=100_000&delay=0')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.content) == 100_000
        # One sleep for the initial delay plus a bounded number of chunk sleeps.
        assert len(delays) <= 101


class TestLinks:
    """Tests for the /links endpoint."""

    def test_html_page(self, client):
        response = client.get('/links/5/0')
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-type'].startswith('text/html')
        assert '<a href=' in response.text


@pytest.mark.skip(reason='Endpoint raises NotImplementedError')
class TestRange:
    """Tests for the /range endpoint (unimplemented)."""

    pass


class TestStreamBytes:
    """Tests for the /stream-bytes endpoint."""

    def test_size(self, client):
        n = 2**10
        response = client.get(f'/stream-bytes/{n}')
        assert response.status_code == status.HTTP_200_OK
        size = sum(len(con) for con in response.iter_bytes())
        assert size == n

    def test_seed_deterministic(self, client):
        n = 100
        response_a = client.get(f'/stream-bytes/{n}?seed=42')
        response_b = client.get(f'/stream-bytes/{n}?seed=42')
        assert response_a.content == response_b.content


class TestUuid:
    """Tests for the /uuid endpoint."""

    def test_valid_uuid4(self, client):
        response = client.get('/uuid')
        assert response.status_code == status.HTTP_200_OK
        uuid.UUID(response.json()['uuid'])
