from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_openapi_contains_expected_endpoints():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    assert "/v1/summarize" in openapi["paths"]
    assert "/v1/health" in openapi["paths"]
    assert "/" in openapi["paths"]

def test_openapi_documents_summary_endpoint():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    summarize = openapi["paths"]["/v1/summarize"]["post"]

    assert summarize["summary"] == "Generate AI Summary"

    assert "200" in summarize["responses"]
    assert "400" in summarize["responses"]
    assert "422" in summarize["responses"]
    assert "429" in summarize["responses"]
    assert "500" in summarize["responses"]

def test_openapi_documents_response_schemas():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    schemas = openapi["components"]["schemas"]

    assert "SummaryRequest" in schemas
    assert "SummaryResponse" in schemas
    assert "HealthResponse" in schemas
    assert "HomeResponse" in schemas
    assert "APIResponse_SummaryResponse_" in schemas