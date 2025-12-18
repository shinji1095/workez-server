from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from apps.common.responses import success_envelope
from apps.common.pagination import parse_page_params
from apps.common.permissions import RoleAdminOnly, RoleAtLeastUser

from .serializers import (
    CreateUsersRequestSerializer,
    PartialUpdateUsersRequestSerializer,
    UserSerializer,
)
from . import services

class UsersListCreateView(APIView):
    """/users GET, POST"""

    def get_permissions(self):
        # listUsers: 管理者≧
        if self.request.method == "GET":
            return [RoleAdminOnly()]
        # createUsers: 一般≧
        return [RoleAtLeastUser()]

    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items, total = services.list_users(page, page_size)
        data = {
            "items": UserSerializer(items, many=True).data,
            "page": page,
            "page_size": page_size,
            "total": total,
        }
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

    def post(self, request):
        ser = CreateUsersRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = services.create_user(ser.validated_data)
        return Response(success_envelope(request, UserSerializer(user).data), status=status.HTTP_201_CREATED)

class UsersDetailView(APIView):
    """/users/{userId} PATCH, DELETE"""

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [RoleAdminOnly()]
        return [RoleAtLeastUser()]

    def patch(self, request, userId: str):
        ser = PartialUpdateUsersRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = services.partial_update_user(userId, ser.validated_data)
        return Response(success_envelope(request, UserSerializer(user).data), status=status.HTTP_200_OK)

    def delete(self, request, userId: str):
        services.delete_user(userId)
        data = {"deleted": True, "user_id": userId}
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)
