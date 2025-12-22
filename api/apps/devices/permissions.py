from rest_framework.permissions import BasePermission  # type: ignore
from rest_framework.request import Request  # type: ignore
from rest_framework.exceptions import PermissionDenied, NotAuthenticated  # type: ignore
from apps.common.permissions import ROLE_ORDER, _role_value  # type: ignore

class RoleDeviceOrAdmin(BasePermission):
    """CSVで権限未記載のデバイス→バックエンド送信系に暫定適用。

    - device role or admin role
    - NOTE: CSV権限が空のため、READMEに明記して見直し前提。
    """

    def has_permission(self, request: Request, view) -> bool:
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            raise NotAuthenticated()
        v = _role_value(request)
        if v in (ROLE_ORDER["device"], ROLE_ORDER["admin"]):
            return True
        raise PermissionDenied()
