def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Hello, Roshan! My first FastAPI app is running."
    }


def test_health(client):
    response = client.get("/v1/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }