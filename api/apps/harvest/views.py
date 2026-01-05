from __future__ import annotations

from datetime import datetime, time
from datetime import date
from uuid import UUID

from django.utils import timezone
from rest_framework.exceptions import ValidationError  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework import status  # type: ignore

from apps.common.pagination import paginate_list, parse_page_params
from apps.common.permissions import RoleAdminOnly, RoleAtLeastUser
from apps.common.responses import success_response

from apps.devices.permissions import RoleDeviceOnly
from .models import HarvestRecord, Rank, Size
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

def _parse_path_date(raw: str) -> date:
    try:
        return date.fromisoformat(raw)
    except ValueError as e:
        raise ValidationError({"date": "Invalid ISO date (YYYY-MM-DD)."}) from e


class TabletHarvestView(APIView):
    permission_classes = [RoleAtLeastUser]

    def _get_optional_query(self, request, name: str) -> str | None:
        value = request.query_params.get(name)
        if value is None:
            return None
        value = str(value).strip()
        return value or None

    def _get_required_query(self, request, name: str) -> str:
        value = request.query_params.get(name)
        if value is None or not str(value).strip():
            raise ValidationError({name: "required"})
        return str(value).strip()

    def _get_optional_uuid_query(self, request, name: str) -> UUID | None:
        value = self._get_optional_query(request, name)
        if not value:
            return None
        try:
            return UUID(value)
        except ValueError as e:
            raise ValidationError({name: "invalid uuid"}) from e

    def _require_size_rank(self, size_id: str, rank_id: str) -> tuple[Size, Rank]:
        size = Size.objects.filter(size_id=size_id).first()
        if not size:
            from rest_framework.exceptions import NotFound  # type: ignore

            raise NotFound(detail={"size": "not found"})
        rank = Rank.objects.filter(rank_id=rank_id).first()
        if not rank:
            from rest_framework.exceptions import NotFound  # type: ignore

            raise NotFound(detail={"rank": "not found"})
        return size, rank

    def _lookup(self, d: date, lot: str, size: Size, rank: Rank) -> HarvestRecord | None:
        return (
            HarvestRecord.objects.filter(
                event_id__isnull=True,
                lot_name=lot,
                size=size,
                rank=rank,
                occurred_at__date=d,
            )
            .order_by("-created_at")
            .first()
        )

    def _require_tablet_record(self, record_id: UUID) -> HarvestRecord:
        rec = (
            HarvestRecord.objects.filter(id=record_id, event_id__isnull=True)
            .select_related("size", "rank")
            .first()
        )
        if not rec:
            from rest_framework.exceptions import NotFound  # type: ignore

            raise NotFound()
        return rec

    def post(self, request, date: str):
        d = _parse_path_date(date)
        lot = self._get_required_query(request, "lot")
        size_id = self._get_required_query(request, "size")
        rank_id = self._get_required_query(request, "rank")

        count = request.data.get("count")
        if isinstance(count, bool) or not isinstance(count, int):
            raise ValidationError({"count": "must be an integer"})
        if count < 0:
            raise ValidationError({"count": "must be >= 0"})

        size, rank = self._require_size_rank(size_id, rank_id)
        occurred_at = timezone.make_aware(
            datetime.combine(d, time.min),
            timezone.get_current_timezone(),
        )

        existing = self._lookup(d, lot, size, rank)
        if existing:
            existing.count = count
            existing.occurred_at = occurred_at
            existing.save(update_fields=["count", "occurred_at"])
            rec = existing
            http_status = status.HTTP_200_OK
        else:
            rec = HarvestRecord.objects.create(
                event_id=None,
                lot_name=lot,
                size=size,
                rank=rank,
                count=count,
                occurred_at=occurred_at,
            )
            http_status = status.HTTP_201_CREATED

        out = {
            "date": d.isoformat(),
            "lot": lot,
            "size": size.size_id,
            "rank": rank.rank_id,
            "count": rec.count,
        }
        return Response(success_response(request, out), status=http_status)

    def get(self, request, date: str):
        d = _parse_path_date(date)
        lot = self._get_optional_query(request, "lot")
        size_id = self._get_optional_query(request, "size")
        rank_id = self._get_optional_query(request, "rank")

        if lot and size_id and rank_id:
            size, rank = self._require_size_rank(size_id, rank_id)
            rec = self._lookup(d, lot, size, rank)
            if not rec:
                from rest_framework.exceptions import NotFound  # type: ignore

                raise NotFound()

            out = {
                "date": d.isoformat(),
                "lot": lot,
                "size": size.size_id,
                "rank": rank.rank_id,
                "count": rec.count,
            }
            return Response(success_response(request, out), status=status.HTTP_200_OK)

        page, page_size = parse_page_params(request.query_params)
        sort = (self._get_optional_query(request, "sort") or "default").lower()
        order = (self._get_optional_query(request, "order") or "asc").lower()

        if order not in ("asc", "desc"):
            raise ValidationError({"order": "must be 'asc' or 'desc'"})

        sort_map = {
            "lot": "lot_name",
            "size": "size__size_id",
            "rank": "rank__rank_id",
            "count": "count",
            "occurred_at": "occurred_at",
            "created_at": "created_at",
        }

        qs = HarvestRecord.objects.filter(event_id__isnull=True, occurred_at__date=d).select_related("size", "rank")
        if lot:
            qs = qs.filter(lot_name=lot)
        if size_id:
            size = Size.objects.filter(size_id=size_id).first()
            if not size:
                from rest_framework.exceptions import NotFound  # type: ignore

                raise NotFound(detail={"size": "not found"})
            qs = qs.filter(size=size)
        if rank_id:
            rank = Rank.objects.filter(rank_id=rank_id).first()
            if not rank:
                from rest_framework.exceptions import NotFound  # type: ignore

                raise NotFound(detail={"rank": "not found"})
            qs = qs.filter(rank=rank)

        if sort == "default":
            fields = ["lot_name", "size__size_id", "rank__rank_id", "id"]
            if order == "desc":
                fields = [f"-{f}" for f in fields[:-1]] + [fields[-1]]
            qs = qs.order_by(*fields)
        else:
            field = sort_map.get(sort)
            if not field:
                raise ValidationError({"sort": f"must be one of: {', '.join(['default', *sort_map.keys()])}"})
            prefix = "-" if order == "desc" else ""
            qs = qs.order_by(f"{prefix}{field}", "id")

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        items = HarvestRecordSerializer(qs[start:end], many=True).data
        payload = {"items": items, "page": page, "page_size": page_size, "total": total}
        return Response(success_response(request, payload), status=status.HTTP_200_OK)

    def put(self, request, date: str):
        record_id = self._get_optional_uuid_query(request, "id")
        if record_id:
            rec = self._require_tablet_record(record_id)

            raw_date = request.data.get("date")
            if raw_date is None or (isinstance(raw_date, str) and not raw_date.strip()):
                new_date = rec.occurred_at.astimezone(timezone.get_current_timezone()).date()
            else:
                try:
                    new_date = _parse_path_date(str(raw_date).strip())
                except ValidationError as e:
                    raise ValidationError({"date": e.detail.get("date", "Invalid ISO date (YYYY-MM-DD).")}) from e

            raw_lot = request.data.get("lot")
            if raw_lot is None:
                new_lot = rec.lot_name
            else:
                new_lot = str(raw_lot).strip()
                if not new_lot:
                    raise ValidationError({"lot": "must not be blank"})

            raw_size = request.data.get("size")
            new_size_id = rec.size.size_id if raw_size is None else str(raw_size).strip()
            if not new_size_id:
                raise ValidationError({"size": "must not be blank"})

            raw_rank = request.data.get("rank")
            new_rank_id = rec.rank.rank_id if raw_rank is None else str(raw_rank).strip()
            if not new_rank_id:
                raise ValidationError({"rank": "must not be blank"})

            count = request.data.get("count", rec.count)
            if isinstance(count, bool) or not isinstance(count, int):
                raise ValidationError({"count": "must be an integer"})
            if count < 0:
                raise ValidationError({"count": "must be >= 0"})

            size, rank = self._require_size_rank(new_size_id, new_rank_id)
            occurred_at = timezone.make_aware(
                datetime.combine(new_date, time.min),
                timezone.get_current_timezone(),
            )

            conflict = (
                HarvestRecord.objects.filter(
                    event_id__isnull=True,
                    lot_name=new_lot,
                    size=size,
                    rank=rank,
                    occurred_at__date=new_date,
                )
                .exclude(id=rec.id)
                .order_by("-created_at")
                .first()
            )

            if conflict:
                conflict.count = count
                conflict.occurred_at = occurred_at
                conflict.save(update_fields=["count", "occurred_at"])
                rec.delete()
                rec = conflict
            else:
                rec.lot_name = new_lot
                rec.size = size
                rec.rank = rank
                rec.count = count
                rec.occurred_at = occurred_at
                rec.save(update_fields=["lot_name", "size", "rank", "count", "occurred_at"])

            return Response(success_response(request, HarvestRecordSerializer(rec).data), status=status.HTTP_200_OK)

        d = _parse_path_date(date)
        lot = self._get_required_query(request, "lot")
        size_id = self._get_required_query(request, "size")
        rank_id = self._get_required_query(request, "rank")

        count = request.data.get("count")
        if isinstance(count, bool) or not isinstance(count, int):
            raise ValidationError({"count": "must be an integer"})
        if count < 0:
            raise ValidationError({"count": "must be >= 0"})

        size, rank = self._require_size_rank(size_id, rank_id)
        rec = self._lookup(d, lot, size, rank)
        if not rec:
            from rest_framework.exceptions import NotFound  # type: ignore

            raise NotFound()

        occurred_at = timezone.make_aware(
            datetime.combine(d, time.min),
            timezone.get_current_timezone(),
        )
        rec.count = count
        rec.occurred_at = occurred_at
        rec.save(update_fields=["count", "occurred_at"])

        out = {
            "date": d.isoformat(),
            "lot": lot,
            "size": size.size_id,
            "rank": rank.rank_id,
            "count": rec.count,
        }
        return Response(success_response(request, out), status=status.HTTP_200_OK)

    def delete(self, request, date: str):
        record_id = self._get_optional_uuid_query(request, "id")
        if record_id:
            rec = self._require_tablet_record(record_id)
            rec.delete()
            out = {"deleted": True, "id": str(record_id)}
            return Response(success_response(request, out), status=status.HTTP_200_OK)

        d = _parse_path_date(date)
        lot = self._get_required_query(request, "lot")
        size_id = self._get_required_query(request, "size")
        rank_id = self._get_required_query(request, "rank")

        size, rank = self._require_size_rank(size_id, rank_id)
        rec = self._lookup(d, lot, size, rank)
        if not rec:
            from rest_framework.exceptions import NotFound  # type: ignore

            raise NotFound()

        rec.delete()
        out = {
            "deleted": True,
            "date": d.isoformat(),
            "lot": lot,
            "size": size.size_id,
            "rank": rank.rank_id,
        }
        return Response(success_response(request, out), status=status.HTTP_200_OK)


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
        items = services.list_aggregate_total(period_type="daily")
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class ListHarvestWeeklyView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_total(period_type="weekly")
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class ListHarvestMonthlyView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_total(period_type="monthly")
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class RetrieveHarvestDailySizeView(APIView):
    def get_permissions(self):
        if self.request.method == "PATCH":
            return [RoleAdminOnly()]
        return [RoleAtLeastUser()]

    def get(self, request, size_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_size(period_type="daily", size_id=size_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))

    def patch(self, request, size_id: str):
        period = _period_from_date("daily", _date_param_or_today(request))
        s = UpdateHarvestAmountOverrideRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        ov = services.upsert_override(
            period_type="daily",
            size_id=size_id,
            period=period,
            total_count=s.validated_data["count"],
        )
        out = {"period": ov.period, "size_id": ov.size_id, "size_name": ov.size_name, "total_count": ov.total_count}
        return Response(success_response(request, out))


class RetrieveHarvestWeeklySizeView(APIView):
    def get_permissions(self):
        if self.request.method == "PATCH":
            return [RoleAdminOnly()]
        return [RoleAtLeastUser()]

    def get(self, request, size_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_size(period_type="weekly", size_id=size_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))

    def patch(self, request, size_id: str):
        period = _period_from_date("weekly", _date_param_or_today(request))
        s = UpdateHarvestAmountOverrideRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        ov = services.upsert_override(
            period_type="weekly",
            size_id=size_id,
            period=period,
            total_count=s.validated_data["count"],
        )
        out = {"period": ov.period, "size_id": ov.size_id, "size_name": ov.size_name, "total_count": ov.total_count}
        return Response(success_response(request, out))


class RetrieveHarvestMonthlySizeView(APIView):
    def get_permissions(self):
        if self.request.method == "PATCH":
            return [RoleAdminOnly()]
        return [RoleAtLeastUser()]

    def get(self, request, size_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_size(period_type="monthly", size_id=size_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))

    def patch(self, request, size_id: str):
        period = _period_from_date("monthly", _date_param_or_today(request))
        s = UpdateHarvestAmountOverrideRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        ov = services.upsert_override(
            period_type="monthly",
            size_id=size_id,
            period=period,
            total_count=s.validated_data["count"],
        )
        out = {"period": ov.period, "size_id": ov.size_id, "size_name": ov.size_name, "total_count": ov.total_count}
        return Response(success_response(request, out))
