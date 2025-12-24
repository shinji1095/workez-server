from __future__ import annotations

from datetime import date

from django.utils import timezone
from rest_framework.exceptions import ValidationError  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore

from apps.common.pagination import paginate_list, parse_page_params
from apps.common.permissions import RoleAdminOnly, RoleAtLeastUser
from apps.common.responses import success_response

from apps.devices.permissions import RoleDeviceOnly
from .serializers import (
    CreateHarvestAmountAddRequestSerializer,
    HarvestRecordSerializer,
    UpdateHarvestAmountOverrideRequestSerializer,
)
from . import services


def _period_from_date(period_type: str, d: date) -> str:
    if period_type == "daily":
        return d.isoformat()
    if period_type == "monthly":
        return f"{d.year:04d}-{d.month:02d}"
    if period_type == "weekly":
        y, w, _ = d.isocalendar()
        return f"{y:04d}-W{w:02d}"
    raise ValueError(f"Unknown period_type: {period_type}")


def _date_param_or_today(request) -> date:
    raw = request.query_params.get("date")
    if raw:
        try:
            return date.fromisoformat(raw)
        except ValueError as e:
            raise ValidationError({"date": "Invalid ISO date (YYYY-MM-DD)."}) from e
    return timezone.localdate()


class CreateHarvestAmountAddView(APIView):
    permission_classes = [RoleDeviceOnly]

    def post(self, request):
        # DEBUG: log auth/user for troubleshooting
        try:
            print(f"[CreateHarvestAmountAddView.post] user={getattr(request.user,'sub',None)} role={getattr(request.user,'role',None)} auth={getattr(request,'auth',None)}")
        except Exception:
            print("[CreateHarvestAmountAddView.post] cannot print user/auth")

        # enforce device-only permission explicitly to avoid unexpected overrides
        auth = getattr(request, "auth", None)
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            from rest_framework.exceptions import NotAuthenticated

            raise NotAuthenticated()

        role_from_auth = None
        try:
            from collections.abc import Mapping

            if isinstance(auth, Mapping):
                role_from_auth = auth.get("role")
        except Exception:
            role_from_auth = None

        role = role_from_auth or getattr(user, "role", None)
        if str(role).lower() != "device":
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied()

        s = CreateHarvestAmountAddRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        rec = services.add_record(**s.validated_data)
        out = HarvestRecordSerializer(rec).data
        return Response(success_response(request, out), status=201)


class ListHarvestDailyView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate(period_type="daily")
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class ListHarvestWeeklyView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate(period_type="weekly")
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class ListHarvestMonthlyView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate(period_type="monthly")
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class ListHarvestDailyCategoryView(APIView):
    def get_permissions(self):
        if self.request.method == "PATCH":
            return [RoleAdminOnly()]
        return [RoleAtLeastUser()]

    def get(self, request, category_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_category(period_type="daily", category_id=category_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))

    def patch(self, request, category_id: str):
        period = _period_from_date("daily", _date_param_or_today(request))
        s = UpdateHarvestAmountOverrideRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        ov = services.upsert_override(
            period_type="daily",
            category_id=category_id,
            period=period,
            total_count=s.validated_data["total_count"],
        )
        out = {
            "id": str(ov.id),
            "period_type": ov.period_type,
            "category_id": ov.category_id,
            "period": ov.period,
            "total_count": ov.total_count,
        }
        return Response(success_response(request, out))


class ListHarvestWeeklyCategoryView(APIView):
    def get_permissions(self):
        if self.request.method == "PATCH":
            return [RoleAdminOnly()]
        return [RoleAtLeastUser()]

    def get(self, request, category_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_category(period_type="weekly", category_id=category_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))

    def patch(self, request, category_id: str):
        period = _period_from_date("weekly", _date_param_or_today(request))
        s = UpdateHarvestAmountOverrideRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        ov = services.upsert_override(
            period_type="weekly",
            category_id=category_id,
            period=period,
            total_count=s.validated_data["total_count"],
        )
        out = {
            "id": str(ov.id),
            "period_type": ov.period_type,
            "category_id": ov.category_id,
            "period": ov.period,
            "total_count": ov.total_count,
        }
        return Response(success_response(request, out))


class ListHarvestMonthlyCategoryView(APIView):
    def get_permissions(self):
        if self.request.method == "PATCH":
            return [RoleAdminOnly()]
        return [RoleAtLeastUser()]

    def get(self, request, category_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_category(period_type="monthly", category_id=category_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))

    def patch(self, request, category_id: str):
        period = _period_from_date("monthly", _date_param_or_today(request))
        s = UpdateHarvestAmountOverrideRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        ov = services.upsert_override(
            period_type="monthly",
            category_id=category_id,
            period=period,
            total_count=s.validated_data["total_count"],
        )
        out = {
            "id": str(ov.id),
            "period_type": ov.period_type,
            "category_id": ov.category_id,
            "period": ov.period,
            "total_count": ov.total_count,
        }
        return Response(success_response(request, out))
