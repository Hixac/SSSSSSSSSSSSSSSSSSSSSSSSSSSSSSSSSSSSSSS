#from fastapi.testclient import TestClient
#from src.app.main import app
#
#client = TestClient(app)
#
#
#def test_health():
#    response = client.get("/api/v1/health/")
#    assert response.status_code == 200
#
#def test_returns_200_for_valid_data():
#    data = {"name": "Andrey", "surname": "Hlystov", "patronymic": "Dmitrievich", \
#            "email": "ddd@gmail.com", "password": "1234"}
#    response = client.post("/users/", json=data)
#
#    assert response.status_code == 200
#
#def test_returns_422_for_invalid_data():
#    data = {"name": "Andrey", "surname": "Hlystov", "email": "ddd@gmail.com"}
#    response = client.post("/users/", json=data)
#
#    assert response.status_code == 422
