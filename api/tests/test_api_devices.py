import pytest

pytestmark = pytest.mark.django_db

def test_create_device_and_battery_flow(admin_client, device_client, user_client):
    resp = admin_client.post("/devices", {"id": "D1", "name": "Device1", "status": "active"}, format="json")
    assert resp.status_code == 201

    # post battery by device
    resp2 = device_client.post("/devices/D1/battery", {"percent": 50, "is_charging": False}, format="json")
    assert resp2.status_code == 201

    # get battery by user
    resp3 = user_client.get("/devices/D1/battery")
    assert resp3.status_code == 200
