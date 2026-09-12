"""Tag: Auth"""

from base64 import b64encode

from starlette import status


def test_basic_auth_valid(client):
    credentials = b64encode(b'admin:secret').decode()
    response = client.get('/basic-auth/admin/secret', headers={'Authorization': f'Basic {credentials}'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'authenticated': True, 'user': 'admin'}


def test_basic_auth_wrong_password(client):
    credentials = b64encode(b'admin:wrong').decode()
    response = client.get('/basic-auth/admin/secret', headers={'Authorization': f'Basic {credentials}'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.headers['www-authenticate'] == 'Basic'


def test_basic_auth_missing_header(client):
    response = client.get('/basic-auth/admin/secret')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.headers['www-authenticate'] == 'Basic'
