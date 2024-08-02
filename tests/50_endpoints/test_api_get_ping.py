from fastapi.testclient import TestClient


def test_get_ping(client: TestClient):
    with client:
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "Pong!"}
