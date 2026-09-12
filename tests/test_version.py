"""Version metadata tests."""

import httpbinx


def test_package_and_openapi_version_are_1_12_0(client):
    assert httpbinx.__version__ == '1.12.0'
    assert httpbinx.app.version == '1.12.0'
    assert client.get('/openapi.json').json()['info']['version'] == '1.12.0'
