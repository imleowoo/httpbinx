# -*- coding: utf-8 -*-
"""
Tag: Request Inspection
"""
from fastapi.testclient import TestClient
from starlette import status

from httpbinx import app

client = TestClient(app)


def test_headers():
    response = client.get('/headers')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['headers']['user-agent'] == 'testclient'


def test_ip():
    response = client.get('/ip')
    assert response.status_code == status.HTTP_200_OK
    # assert response.json()['origin'] == 'testclient'


def test_user_agent():
    response = client.get('/user-agent')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['user-agent'] == 'testclient'

    ua_examples = [
        'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1',
        'Mozilla/5.0 (compatible; Googlebot/2.1; +https://www.google.com/bot.html)',
        'curl/7.64.1',
        'PostmanRuntime/7.26.5'
    ]
    for ua in ua_examples:
        headers = {'User-Agent': ua}
        response = client.get('/user-agent', headers=headers)
        assert response.json()['user-agent'] == ua
