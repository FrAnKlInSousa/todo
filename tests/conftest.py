import pytest
from fastapi.testclient import TestClient

from todo.app import app


@pytest.fixture
def client():
    return TestClient(app)
