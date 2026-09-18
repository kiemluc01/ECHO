from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ok"


def test_readiness_reports_database_dependency() -> None:
    response = client.get("/health/ready")
    assert response.status_code in {200, 503}
    assert response.json()["data"]["status"] in {"ready", "not_ready"}


def test_openapi_describes_api_and_bearer_security() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    document = response.json()
    assert document["info"]["title"] == "ECHO API"
    assert "/v1/me" in document["paths"]
    assert "HTTPBearer" in document["components"]["securitySchemes"]
    assert document["tags"][0]["name"] == "health"
