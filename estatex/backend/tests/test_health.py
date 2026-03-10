import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_health_endpoint_returns_ok():
    client = APIClient()
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.django_db
def test_service_catalog_lists_foundational_services():
    client = APIClient()
    response = client.get("/api/v1/services")

    assert response.status_code == 200
    payload = response.json()
    assert "auth_service" in payload["services"]
    assert "listing_service" in payload["services"]
