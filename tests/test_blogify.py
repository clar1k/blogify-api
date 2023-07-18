from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_resp():
    response = client.get('/')
    assert response.status_code == 400