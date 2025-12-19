from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
from django.conf import settings  # type: ignore
from rest_framework.authentication import BaseAuthentication  # type: ignore
from rest_framework.request import Request  # type: ignore

@dataclass(frozen=True)
class ApiKeyUser:
    """Lightweight authenticated principal used for API-key based auth."""
    role: str  # admin | user | device

    @property
    def is_authenticated(self) -> bool:
        return True

class ApiKeyAuthentication(BaseAuthentication):
    """Authenticate with a simple API key.

    Supported headers:
    - X-API-KEY: <key>
    - Authorization: Bearer <key>

    Keys are configured by environment variables:
    - ADMIN_API_KEY
    - USER_API_KEY
    - DEVICE_API_KEY

    NOTE: This auth scheme is not defined in openapi.yaml yet.
    It is introduced to enforce CSV role constraints (一般≧/管理者≧).
    """

    def authenticate(self, request: Request) -> Optional[Tuple[ApiKeyUser, str]]:
        key = request.headers.get("X-API-KEY")
        if not key:
            auth = request.headers.get("Authorization", "")
            if auth.lower().startswith("bearer "):
                key = auth[7:].strip()

        if not key:
            return None

        if settings.ADMIN_API_KEY and key == settings.ADMIN_API_KEY:
            return ApiKeyUser(role="admin"), key
        if settings.USER_API_KEY and key == settings.USER_API_KEY:
            return ApiKeyUser(role="user"), key
        if settings.DEVICE_API_KEY and key == settings.DEVICE_API_KEY:
            return ApiKeyUser(role="device"), key

        return None
