from fastapi.testclient import TestClient


def test_get_home(client: TestClient):
    with client:
        response = client.get("/")
        assert response.status_code == 200
        with open("src/api/html/home.html", "r") as fp:
            assert response.text == fp.read()
