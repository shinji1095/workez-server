from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Tuple

import jwt
from django.conf import settings  # type: ignore
from rest_framework.authentication import BaseAuthentication  # type: ignore
from rest_framework.exceptions import AuthenticationFailed  # type: ignore

DEFAULT_ALG = "HS256"


def _jwt_signing_key() -> str:
    key = getattr(settings, "JWT_SIGNING_KEY", "")
    return key or settings.SECRET_KEY


def _jwt_algorithm() -> str:
    alg = getattr(settings, "JWT_ALGORITHM", "")
    return alg or DEFAULT_ALG


@dataclass(frozen=True)
class JwtUser:
    sub: str
    role: str

    @property
    def is_authenticated(self) -> bool:
        return True


def issue_jwt(*, sub: str, role: str, lifetime_seconds: int = 3600) -> str:
    """Issue a JWT (mainly for tests)."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=lifetime_seconds)).timestamp()),
    }
    token = jwt.encode(payload, _jwt_signing_key(), algorithm=_jwt_algorithm())
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


class JwtAuthentication(BaseAuthentication):
    """Simple Bearer JWT authentication."""

    keyword = "Bearer"

    def authenticate(self, request) -> Optional[Tuple[JwtUser, Any]]:
        header = request.headers.get("Authorization") or ""
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        token = parts[1]
        try:
            payload = jwt.decode(token, _jwt_signing_key(), algorithms=[_jwt_algorithm()])
        except Exception as e:
            # Convert any decode/validation error to a proper 401.
            raise AuthenticationFailed("Invalid token") from e

        sub = payload.get("sub")
        role = payload.get("role")
        if not sub or not role:
            raise AuthenticationFailed("Invalid token payload")

        return JwtUser(sub=str(sub), role=str(role)), payload

    def authenticate_header(self, request) -> str:
        # Returning a non-empty header makes DRF respond 401 (not 403) when unauthenticated.
        return self.keyword
