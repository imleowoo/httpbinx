import pytest
from fastapi.testclient import TestClient

from httpbinx import app


@pytest.fixture
def client():
    return TestClient(app)
