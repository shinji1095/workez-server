from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from apps.common.responses import success_envelope
from apps.common.pagination import parse_page_params
from apps.common.permissions import RoleAdminOnly, RoleAtLeastUser

from .serializers import (
    DeviceSerializer,
    CreateDeviceRequestSerializer,
    BatteryUpdateRequestSerializer,
    BatteryLatestSerializer,
    AlarmCreateRequestSerializer,
    AlarmItemSerializer,
    AlarmStatusSerializer,
)
from . import services
from .permissions import RoleDeviceOrAdmin

class DevicesListCreateView(APIView):
    """/devices GET, POST (管理者≧)"""
    permission_classes = [RoleAdminOnly]

    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items, total = services.list_devices(page, page_size)
        data = {
            "items": DeviceSerializer(items, many=True).data,
            "page": page,
            "page_size": page_size,
            "total": total,
        }
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

    def post(self, request):
        ser = CreateDeviceRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        device = services.create_device(ser.validated_data)
        return Response(success_envelope(request, DeviceSerializer(device).data), status=status.HTTP_201_CREATED)

class DevicesDeleteView(APIView):
    """/devices/{deviceId} DELETE (管理者≧)"""
    permission_classes = [RoleAdminOnly]

    def delete(self, request, deviceId: str):
        services.delete_device(deviceId)
        data = {"deleted": True, "device_id": deviceId}
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

class DevicesBatteryView(APIView):
    """/devices/{deviceId}/battery GET (一般≧), POST (TBD)"""

    def get_permissions(self):
        if self.request.method == "GET":
            return [RoleAtLeastUser()]
        return [RoleDeviceOrAdmin()]

    def get(self, request, deviceId: str):
        latest = services.get_battery_latest(deviceId)
        if latest is None:
            data = {
                "device_id": deviceId,
                "percent": 0,
                "voltage_mv": None,
                "is_charging": False,
                "updated_at": None,
            }
            # OpenAPI requires updated_at; returning null would violate.
            # To avoid schema mismatch, treat missing as 404.
            from rest_framework.exceptions import NotFound  # type: ignore
            raise NotFound("battery status not found")
        data = {
            "device_id": deviceId,
            "percent": latest.percent,
            "voltage_mv": latest.voltage_mv,
            "is_charging": latest.is_charging,
            "updated_at": latest.updated_at,
        }
        return Response(success_envelope(request, BatteryLatestSerializer(data).data), status=status.HTTP_200_OK)

    def post(self, request, deviceId: str):
        ser = BatteryUpdateRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        latest = services.upsert_battery(deviceId, ser.validated_data)
        data = {
            "device_id": deviceId,
            "percent": latest.percent,
            "voltage_mv": latest.voltage_mv,
            "is_charging": latest.is_charging,
            "updated_at": latest.updated_at,
        }
        return Response(success_envelope(request, data), status=status.HTTP_201_CREATED)

class DevicesAlermView(APIView):
    """/devices/{deviceId}/alerm GET (一般≧), POST (TBD)"""

    def get_permissions(self):
        if self.request.method == "GET":
            return [RoleAtLeastUser()]
        return [RoleDeviceOrAdmin()]

    def get(self, request, deviceId: str):
        status_dict = services.get_alarm_status(deviceId)
        data = {
            "device_id": status_dict["device_id"],
            "has_active_alarm": status_dict["has_active_alarm"],
            "severity": status_dict["severity"],
            "last_alarm_at": status_dict["last_alarm_at"],
            "active_alarms": AlarmItemSerializer(status_dict["active_alarms"], many=True).data if status_dict["has_active_alarm"] else [],
        }
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

    def post(self, request, deviceId: str):
        ser = AlarmCreateRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        alarm = services.create_alarm(deviceId, ser.validated_data)
        return Response(success_envelope(request, AlarmItemSerializer(alarm).data), status=status.HTTP_201_CREATED)

class DevicesAlermDetailView(APIView):
    """/devices/{deviceId}/alerm/detail GET (一般≧)"""
    permission_classes = [RoleAtLeastUser]

    def get(self, request, deviceId: str):
        page, page_size = parse_page_params(request.query_params)
        items, total = services.list_alarm_items(deviceId, page, page_size)
        data = {
            "items": AlarmItemSerializer(items, many=True).data,
            "page": page,
            "page_size": page_size,
            "total": total,
        }
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)
