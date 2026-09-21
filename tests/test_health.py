def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Hello, Roshan! My first FastAPI app is running."
    }


def test_health(client):

    response = client.get("/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert set(data.keys()) == {"status"}
    assert data["status"] == "healthy"

def test_home_response_headers(client):

    response = client.get("/")

    assert response.status_code == 200

    assert "X-Request-ID" in response.headers
    assert "X-Process-Time" in response.headers

    assert response.headers["X-Request-ID"] != ""
    assert response.headers["X-Process-Time"] != ""

def test_request_id_is_unique(client):
    response_1 = client.get("/")
    response_2 = client.get("/")

    request_id_1 = response_1.headers["X-Request-ID"]
    request_id_2 = response_2.headers["X-Request-ID"]

    assert request_id_1 != request_id_2

def test_process_time_header_is_numeric(client):
    response = client.get("/")

    assert response.status_code == 200

    process_time = response.headers["X-Process-Time"]

    assert float(process_time) >= 0

def test_cors_allows_frontend_origin(client):

    response = client.options(
        "/v1/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        }
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_rejects_unknown_origin(client):

    response = client.options(
        "/v1/health",
        headers={
            "Origin": "http://malicious-site.example",
            "Access-Control-Request-Method": "GET",
        }
    )

    assert "access-control-allow-origin" not in response.headers
