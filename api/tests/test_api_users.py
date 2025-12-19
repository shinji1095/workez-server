import pytest

pytestmark = pytest.mark.django_db

def test_create_user_and_list(admin_client, user_client):
    # create (一般≧)
    resp = user_client.post("/users", {"email": "x@example.com", "name": "X"}, format="json")
    assert resp.status_code == 201

    # list (管理者≧)
    resp2 = admin_client.get("/users?page=1&page_size=10")
    assert resp2.status_code == 200
    body = resp2.json()
    assert body["status"] == "success"
    assert "items" in body["data"]
