from __future__ import annotations

from rest_framework.permissions import BasePermission  # type: ignore

from apps.common.permissions import ROLE_ORDER, _role_value


class RoleDeviceOnly(BasePermission):
    """Allow only device role."""

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return False
        return _role_value(user) == ROLE_ORDER.get("device", 1)
