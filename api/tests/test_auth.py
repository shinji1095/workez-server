import pytest

pytestmark = pytest.mark.django_db

def test_unauthorized_without_key(api_client):
    resp = api_client.get("/users?page=1&page_size=1")
    assert resp.status_code == 401
    assert "error" in resp.json()

def test_forbidden_when_role_insufficient(user_client):
    resp = user_client.get("/users?page=1&page_size=1")
    assert resp.status_code == 403
