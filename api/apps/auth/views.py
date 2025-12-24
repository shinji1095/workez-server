from __future__ import annotations

from typing import Optional

from django.conf import settings  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.exceptions import NotAuthenticated  # type: ignore
from rest_framework.permissions import AllowAny  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore

from apps.common.auth import issue_jwt
from apps.common.responses import success_envelope

from .serializers import CreateAuthTokenRequestSerializer


def _extract_api_key(request) -> Optional[str]:
    api_key = request.headers.get("X-API-KEY")
    if api_key:
        return api_key.strip()

    auth_header = request.headers.get("Authorization") or ""
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        return token or None

    return None


def _role_from_api_key(api_key: str) -> Optional[str]:
    key_map = {}
    if getattr(settings, "ADMIN_API_KEY", ""):
        key_map[settings.ADMIN_API_KEY] = "admin"
    if getattr(settings, "USER_API_KEY", ""):
        key_map[settings.USER_API_KEY] = "user"
    if getattr(settings, "DEVICE_API_KEY", ""):
        key_map[settings.DEVICE_API_KEY] = "device"
    return key_map.get(api_key)


class AuthTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_authenticate_header(self, request) -> str:
        # Ensure NotAuthenticated returns 401 instead of 403.
        return "ApiKey"

    def post(self, request):
        api_key = _extract_api_key(request)
        if not api_key:
            raise NotAuthenticated()

        role = _role_from_api_key(api_key)
        if role is None:
            raise NotAuthenticated()

        ser = CreateAuthTokenRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        sub = ser.validated_data["sub"]

        ttl = int(getattr(settings, "JWT_ACCESS_TOKEN_LIFETIME_SECONDS", 3600))
        token = issue_jwt(sub=sub, role=role, lifetime_seconds=ttl)
        data = {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": ttl,
            "sub": sub,
            "role": role,
        }
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)
