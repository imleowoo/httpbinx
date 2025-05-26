"""
Tag: Images
"""
from fastapi.testclient import TestClient

from httpbinx import app

client = TestClient(app)


def test_image():
    response = client.get('/image')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('image')


def test_image_png():
    response = client.get('/image/png')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('image/png')


def test_image_jpeg():
    response = client.get('/image/jpeg')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('image/jpeg')


def test_image_webp():
    response = client.get('/image/webp')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('image/webp')


def test_image_svg():
    response = client.get('/image/svg')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('image/svg')
