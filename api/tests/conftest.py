import pytest
from rest_framework.test import APIClient  # type: ignore
from django.conf import settings  # type: ignore

@pytest.fixture(autouse=True)
def _set_api_keys(settings):  # noqa: D401
    settings.ADMIN_API_KEY = "admin-test-key"
    settings.USER_API_KEY = "user-test-key"
    settings.DEVICE_API_KEY = "device-test-key"
    return settings

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_client(api_client):
    api_client.credentials(HTTP_X_API_KEY="admin-test-key")
    return api_client

@pytest.fixture
def user_client(api_client):
    api_client.credentials(HTTP_X_API_KEY="user-test-key")
    return api_client

@pytest.fixture
def device_client(api_client):
    api_client.credentials(HTTP_X_API_KEY="device-test-key")
    return api_client
