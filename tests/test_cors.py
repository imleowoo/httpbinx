"""CORS configuration tests."""

ORIGIN = 'https://evil.example.com'


def test_wildcard_origin_is_returned_as_is(client):
    """A wildcard allowlist is echoed literally, not per-request origin."""
    response = client.get('/get', headers={'Origin': ORIGIN})

    assert response.headers['access-control-allow-origin'] == '*'


def test_credentials_are_not_allowed_for_any_origin(client):
    """Credentials must not be combined with a wildcard origin allowlist."""
    response = client.get('/get', headers={'Origin': ORIGIN})

    assert 'access-control-allow-credentials' not in response.headers


def test_preflight_does_not_allow_credentials(client):
    """Preflight responses must not advertise credentialed cross-origin access."""
    response = client.options(
        '/get',
        headers={
            'Origin': ORIGIN,
            'Access-Control-Request-Method': 'GET',
        },
    )

    assert response.headers['access-control-allow-origin'] == '*'
    assert 'access-control-allow-credentials' not in response.headers
