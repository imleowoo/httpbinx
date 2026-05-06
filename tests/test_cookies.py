"""Tag: Cookies"""

from starlette import status


def test_cookies_empty(client):
    response = client.get('/cookies')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'cookies': {}}


def test_cookies_with_value(client):
    client.cookies.set('session', 'abc123')
    response = client.get('/cookies')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['cookies']['session'] == 'abc123'


def test_set_cookies_and_redirect(client):
    response = client.get('/cookies/set?foo=bar&baz=qux', follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert 'foo=bar' in response.headers.get('set-cookie', '')
    assert 'baz=qux' in response.headers.get('set-cookie', '')


def test_set_cookie_and_redirect(client):
    response = client.get('/cookies/set/name/value', follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert 'name=value' in response.headers.get('set-cookie', '')


def test_delete_cookies_and_redirect(client):
    response = client.get('/cookies/delete?session=abc', follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    set_cookie = response.headers.get('set-cookie', '')
    assert 'session=;' in set_cookie or 'session="";' in set_cookie
