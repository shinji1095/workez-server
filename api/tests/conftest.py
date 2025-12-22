import uuid

import pytest
from rest_framework.test import APIClient

from apps.common.jwt import issue_jwt


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_client():
    client = APIClient()
    token = issue_jwt(sub="admin-1", role="admin")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def user_client():
    client = APIClient()
    token = issue_jwt(sub="user-1", role="viewer")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def device_client():
    client = APIClient()
    token = issue_jwt(sub="device-1", role="device")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client
