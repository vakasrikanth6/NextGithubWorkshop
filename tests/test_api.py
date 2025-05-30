"""Test suite for Virtual Power Plant (VPP) API endpoints."""

from fastapi.testclient import TestClient

from src.vpp.main import app

client = TestClient(app)


def test_register_and_list_plants():
    """Test registering a plant and then listing all plants."""
    response = client.post(
        "/plants/",
        json={
            "id": 0,
            "name": "Plant A",
            "max_capacity": 100.0,
            "min_capacity": 10.0,
            "status": "idle",
        },
    )
    assert response.status_code == 200
    plant = response.json()
    assert plant["id"] == 1

    list_resp = client.get("/plants/")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1


def test_aggregate_and_dispatch():
    """Test the aggregate capacity endpoint and the dispatch logic."""
    # Ensure at least one plant exists
    client.post(
        "/plants/",
        json={
            "id": 0,
            "name": "Plant B",
            "max_capacity": 50.0,
            "min_capacity": 5.0,
            "status": "idle",
        },
    )

    agg = client.get("/aggregate/")
    assert agg.status_code == 200
    total = agg.json()["total_available"]
    assert total > 0

    # Dispatch some demand
    dispatch_resp = client.post("/dispatch/", json={"demand": 120.0})
    assert dispatch_resp.status_code == 200
    data = dispatch_resp.json()
    assert "allocations" in data
    assert data["total_dispatched"] <= total
    assert data["unmet_demand"] >= 0
