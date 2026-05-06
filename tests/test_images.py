"""Tag: Images"""

from starlette import status


def test_image_accept_png(client):
    response = client.get('/image', headers={'Accept': 'image/png'})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/png')


def test_image_accept_jpeg(client):
    response = client.get('/image', headers={'Accept': 'image/jpeg'})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/jpeg')


def test_image_accept_webp(client):
    response = client.get('/image', headers={'Accept': 'image/webp'})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/webp')


def test_image_accept_svg(client):
    response = client.get('/image', headers={'Accept': 'image/svg+xml'})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/svg')


def test_image_accept_wildcard(client):
    response = client.get('/image', headers={'Accept': 'image/*'})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/png')


def test_image_accept_any(client):
    response = client.get('/image', headers={'Accept': '*/*'})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/png')


def test_image_accept_not_acceptable(client):
    response = client.get('/image', headers={'Accept': 'text/html'})
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE


def test_image_png(client):
    response = client.get('/image/png')
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/png')


def test_image_jpeg(client):
    response = client.get('/image/jpeg')
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/jpeg')


def test_image_webp(client):
    response = client.get('/image/webp')
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/webp')


def test_image_svg(client):
    response = client.get('/image/svg')
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith('image/svg')
