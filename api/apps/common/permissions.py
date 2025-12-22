from rest_framework.permissions import BasePermission  # type: ignore
from rest_framework.request import Request  # type: ignore
from rest_framework.exceptions import NotAuthenticated, PermissionDenied  # type: ignore

ROLE_ORDER = {
    "device": 1,
    "viewer": 2,
    "user": 2,   # backward-compatible alias
    "admin": 3,
}

def _role_value(request: Request) -> int:
    user = getattr(request, "user", None)
    role = getattr(user, "role", None)
    return ROLE_ORDER.get(str(role), 0)

def _ensure_authenticated(request: Request) -> None:
    user = getattr(request, "user", None)
    if not user or not getattr(user, "is_authenticated", False):
        raise NotAuthenticated()

class RoleAtLeastUser(BasePermission):
    """一般≧ : authenticated user or admin."""

    def has_permission(self, request: Request, view) -> bool:
        _ensure_authenticated(request)
        if _role_value(request) >= ROLE_ORDER["user"]:
            return True
        raise PermissionDenied()

class RoleAdminOnly(BasePermission):
    """管理者≧ : admin only."""

    def has_permission(self, request: Request, view) -> bool:
        _ensure_authenticated(request)
        if _role_value(request) >= ROLE_ORDER["admin"]:
            return True
        raise PermissionDenied()
