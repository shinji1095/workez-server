from datetime import datetime
import re

from django.utils import timezone  # type: ignore
from django.utils.dateparse import parse_date  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.exceptions import ValidationError  # type: ignore

from apps.common.responses import success_envelope
from apps.common.pagination import parse_page_params, paginate_list
from apps.common.permissions import RoleAdminOnly, RoleAtLeastUser

from .serializers import (
    HarvestAddRequestSerializer,
    HarvestRecordSerializer,
    HarvestOverridePatchRequestSerializer,
    HarvestTargetUpdateRequestSerializer,
)
from . import services

def _get_period_from_query(request, period_type: str) -> str:
    """Compute target period for overrides.

    Rules (設計判断 Q14):
    - daily:   date=YYYY-MM-DD (default: today)
    - weekly:  date=YYYY-MM-DD を含む週 (ISO week) (default: today)
    - monthly: month=YYYY-MM (default: this month)
    """

    if period_type in ("daily", "weekly"):
        date_str = request.query_params.get("date")
        if date_str:
            d = parse_date(date_str)
            if d is None:
                raise ValidationError({"date": ["Invalid date format. Use YYYY-MM-DD."]})
        else:
            d = timezone.localdate()

        if period_type == "daily":
            return d.isoformat()

        iso = d.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"

    # monthly
    month_str = request.query_params.get("month_ym") or request.query_params.get("month")
    if month_str:
        if not re.match(r"^\d{4}-\d{2}$", month_str):
            raise ValidationError({"month": ["Invalid month format. Use YYYY-MM."]})
        return month_str

    today = timezone.localdate()
    return f"{today.year:04d}-{today.month:02d}"

class HarvestAmountAddView(APIView):
    """POST /harvest/amount/add (権限CSV未記載)"""
    # 暫定: デバイス送信なので device|admin だけ許可にしたいが、CSV未記載のため一般にも開放しない。
    # ここでは device|admin を許可する。
    from apps.devices.permissions import RoleDeviceOrAdmin
    permission_classes = [RoleDeviceOrAdmin]

    def post(self, request):
        ser = HarvestAddRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rec = services.add_record(ser.validated_data)
        return Response(success_envelope(request, HarvestRecordSerializer(rec).data), status=status.HTTP_201_CREATED)

class HarvestAmountDailyView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate("daily")
        data = paginate_list(items, page, page_size)
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

class HarvestAmountWeeklyView(APIView):
    permission_classes = [RoleAtLeastUser]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate("weekly")
        data = paginate_list(items, page, page_size)
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

class HarvestAmountMonthlyView(APIView):
    permission_classes = [RoleAtLeastUser]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate("monthly")
        data = paginate_list(items, page, page_size)
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

class HarvestAmountDailyCategoryView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [RoleAtLeastUser()]
        return [RoleAdminOnly()]

    def get(self, request, categoryId: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_category("daily", categoryId)
        data = paginate_list(items, page, page_size)
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

    def patch(self, request, categoryId: str):
        ser = HarvestOverridePatchRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        period = _get_period_from_query(request, "daily")
        ov = services.patch_override("daily", categoryId, period, ser.validated_data["total_count"])
        data = {
            "period": ov.period,
            "category_id": ov.category_id,
            "category_name": ov.category_name,
            "total_count": ov.total_count,
        }
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

class HarvestAmountWeeklyCategoryView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [RoleAtLeastUser()]
        return [RoleAdminOnly()]

    def get(self, request, categoryId: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_category("weekly", categoryId)
        data = paginate_list(items, page, page_size)
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

    def patch(self, request, categoryId: str):
        ser = HarvestOverridePatchRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        period = _get_period_from_query(request, "weekly")
        ov = services.patch_override("weekly", categoryId, period, ser.validated_data["total_count"])
        data = {
            "period": ov.period,
            "category_id": ov.category_id,
            "category_name": ov.category_name,
            "total_count": ov.total_count,
        }
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

class HarvestAmountMonthlyCategoryView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [RoleAtLeastUser()]
        return [RoleAdminOnly()]

    def get(self, request, categoryId: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_category("monthly", categoryId)
        data = paginate_list(items, page, page_size)
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

    def patch(self, request, categoryId: str):
        ser = HarvestOverridePatchRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        period = _get_period_from_query(request, "monthly")
        ov = services.patch_override("monthly", categoryId, period, ser.validated_data["total_count"])
        data = {
            "period": ov.period,
            "category_id": ov.category_id,
            "category_name": ov.category_name,
            "total_count": ov.total_count,
        }
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

class HarvestTargetDailyView(APIView):
    permission_classes = [RoleAdminOnly]
    def put(self, request):
        ser = HarvestTargetUpdateRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        t = services.update_target("daily", ser.validated_data["target_count"])
        data = {"target_type": t.target_type, "target_count": t.target_count, "updated_at": t.updated_at}
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

class HarvestTargetWeeklyView(APIView):
    permission_classes = [RoleAdminOnly]
    def put(self, request):
        ser = HarvestTargetUpdateRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        t = services.update_target("weekly", ser.validated_data["target_count"])
        data = {"target_type": t.target_type, "target_count": t.target_count, "updated_at": t.updated_at}
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)

class HarvestTargetMonthlyView(APIView):
    permission_classes = [RoleAdminOnly]
    def put(self, request):
        ser = HarvestTargetUpdateRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        t = services.update_target("monthly", ser.validated_data["target_count"])
        data = {"target_type": t.target_type, "target_count": t.target_count, "updated_at": t.updated_at}
        return Response(success_envelope(request, data), status=status.HTTP_200_OK)
