def test_health_endpoint_returns_success(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert "uptime" in payload
