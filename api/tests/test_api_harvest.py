import pytest

pytestmark = pytest.mark.django_db

def test_harvest_add_and_daily(device_client, user_client, admin_client):
    # prepare price (admin) - CSV: POST /prices/category/{categoryId}
    admin_client.post("/prices/category/C1", {"unit_price_yen": 100, "effective_from": "2025-01-01"}, format="json")

    # add harvest (device)
    resp = device_client.post("/harvest/amount/add", {"device_id": "D1", "category_id": "C1", "count": 3}, format="json")
    assert resp.status_code == 201

    # daily list (user)
    resp2 = user_client.get("/harvest/amount/daily?page=1&page_size=10")
    assert resp2.status_code == 200
