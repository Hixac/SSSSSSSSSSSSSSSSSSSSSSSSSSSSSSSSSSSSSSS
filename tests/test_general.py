from fastapi.testclient import TestClient
import app.main as app

client = TestClient(app.app)


def test_health_check():
    response = client.get("/health_check/")
    assert response.status_code == 200
