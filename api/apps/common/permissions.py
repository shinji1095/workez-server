from __future__ import annotations

from typing import Any, Optional

from rest_framework.permissions import BasePermission  # type: ignore

# device を含める（device < user < admin）
ROLE_ORDER = {"device": 1, "user": 2, "admin": 3}


def _normalize_role(role: Any) -> Optional[str]:
    if role is None:
        return None
    if isinstance(role, str):
        r = role.strip().lower()
        return r or None
    return None


def _role_value(user: Any) -> int:
    role = _normalize_role(getattr(user, "role", None))
    if role is None:
        role = _normalize_role(getattr(user, "api_role", None)) or _normalize_role(getattr(user, "kind", None))

    if role is None:
        if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
            return ROLE_ORDER["admin"]
        return 0

    return ROLE_ORDER.get(role, 0)


class RoleAtLeastUser(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return False
        return _role_value(user) >= ROLE_ORDER["user"]


class RoleAdminOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return False
        return _role_value(user) >= ROLE_ORDER["admin"]
