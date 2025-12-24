import jwt
import pytest
from django.conf import settings


pytestmark = pytest.mark.django_db


def _set_api_keys(settings_obj, *, admin="admin-key", user="user-key", device="device-key"):
    settings_obj.ADMIN_API_KEY = admin
    settings_obj.USER_API_KEY = user
    settings_obj.DEVICE_API_KEY = device


def test_issue_token_with_api_key(api_client, settings):
    _set_api_keys(settings, admin="admin-key", user="", device="")

    resp = api_client.post(
        "/auth/token",
        {"sub": "admin-1"},
        format="json",
        HTTP_X_API_KEY="admin-key",
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "success"
    data = body["data"]
    assert data["role"] == "admin"
    assert data["sub"] == "admin-1"
    assert data["token_type"] == "Bearer"
    assert data["expires_in"] == settings.JWT_ACCESS_TOKEN_LIFETIME_SECONDS

    payload = jwt.decode(
        data["access_token"],
        settings.JWT_SIGNING_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
    assert payload["sub"] == "admin-1"
    assert payload["role"] == "admin"


def test_issue_token_allows_authorization_header(api_client, settings):
    _set_api_keys(settings, admin="", user="user-key", device="")

    resp = api_client.post(
        "/auth/token",
        {"sub": "user-1"},
        format="json",
        HTTP_AUTHORIZATION="Bearer user-key",
    )

    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["role"] == "user"


def test_issue_token_requires_valid_key(api_client, settings):
    _set_api_keys(settings, admin="admin-key", user="", device="")

    resp = api_client.post("/auth/token", {"sub": "admin-1"}, format="json")
    assert resp.status_code == 401

    resp = api_client.post(
        "/auth/token",
        {"sub": "admin-1"},
        format="json",
        HTTP_X_API_KEY="invalid-key",
    )
    assert resp.status_code == 401
