from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from apps.common.permissions import RoleAdminOnly
from apps.common.responses import success_envelope
from apps.users.serializers import UserSerializer
from .serializers import UpdateAdminUsersRequestSerializer
from . import services

class AdminUsersUpdateView(APIView):
    """PUT /admin/users/{userId}"""
    permission_classes = [RoleAdminOnly]

    def put(self, request, userId: str):
        ser = UpdateAdminUsersRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = services.update_admin_user(str(userId), ser.validated_data)
        return Response(success_envelope(request, UserSerializer(user).data), status=status.HTTP_200_OK)
