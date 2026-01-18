from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime, time
from datetime import date
from decimal import Decimal
from io import BytesIO, StringIO
from typing import Any
from uuid import UUID

from django.http import HttpResponse
from django.utils import timezone
from rest_framework.exceptions import NotFound, ValidationError  # type: ignore
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
    UpdateHarvestTargetRequestSerializer,
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


def _get_optional_query_param(request, name: str) -> str | None:
    value = request.query_params.get(name)
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def _require_query_date(request, name: str) -> date:
    raw = request.query_params.get(name)
    if not raw:
        raise ValidationError({name: "required"})
    try:
        return date.fromisoformat(str(raw))
    except ValueError as e:
        raise ValidationError({name: "Invalid ISO date (YYYY-MM-DD)."}) from e


def _format_count(value: Decimal) -> str:
    return str(Decimal(value).quantize(Decimal("0.1")))


def _require_size(size_id: str) -> None:
    if not Size.objects.filter(size_id=size_id).exists():
        raise NotFound(detail={"size_id": "size not found"})


def _require_rank(rank_id: str) -> None:
    if not Rank.objects.filter(rank_id=rank_id).exists():
        raise NotFound(detail={"rank_id": "rank not found"})


def _filter_harvest_records(
    start_date: date,
    end_date: date,
    *,
    lot_name: str | None,
    size_id: str | None,
    rank_id: str | None,
):
    qs = HarvestRecord.objects.filter(
        harvested_at__date__gte=start_date,
        harvested_at__date__lte=end_date,
    ).select_related("size", "rank")
    if lot_name:
        qs = qs.filter(lot_name=lot_name)
    if size_id:
        qs = qs.filter(size_id=size_id)
    if rank_id:
        qs = qs.filter(rank_id=rank_id)
    return qs


def _summarize_records_daily(qs) -> tuple[list[dict], int, Decimal]:
    bucket: dict[str, Decimal] = defaultdict(Decimal)
    record_count = 0
    total_count = Decimal("0.0")
    for rec in qs.iterator():
        record_count += 1
        total_count += Decimal(rec.count)
        period = timezone.localtime(rec.harvested_at).date().isoformat()
        bucket[period] += Decimal(rec.count)
    items = [{"period": key, "total_count": bucket[key]} for key in sorted(bucket.keys())]
    return items, record_count, total_count


def _draw_bar_chart(
    c: Any,
    items: list[dict],
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    c.setLineWidth(1)
    c.rect(x, y, width, height)
    if not items:
        c.setFont("Helvetica", 10)
        c.drawString(x + 6, y + height - 14, "No data")
        return

    values = [float(item["total_count"]) for item in items]
    max_val = max(values) if values else 0.0
    if max_val <= 0:
        max_val = 1.0

    bar_count = len(values)
    gap = min(6.0, width / (bar_count * 4)) if bar_count else 0.0
    bar_width = (width - gap * (bar_count + 1)) / bar_count

    c.setFillColorRGB(0.2, 0.4, 0.7)
    for idx, value in enumerate(values):
        bar_height = (value / max_val) * (height - 20)
        bar_x = x + gap + idx * (bar_width + gap)
        c.rect(bar_x, y + 10, bar_width, bar_height, fill=1, stroke=0)

    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 8)
    step = max(1, int(bar_count / 10)) if bar_count else 1
    for idx, item in enumerate(items):
        if idx % step != 0:
            continue
        label = item["period"]
        label_x = x + gap + idx * (bar_width + gap)
        c.drawString(label_x, y + 2, label)

    c.setFont("Helvetica", 8)
    c.drawRightString(x + width - 4, y + height - 12, _format_count(Decimal(str(max_val))))


def _render_harvest_pdf(
    items: list[dict],
    *,
    start_date: date,
    end_date: date,
    lot_name: str | None,
    size_id: str | None,
    rank_id: str | None,
    record_count: int,
    total_count: Decimal,
) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError("reportlab is required for PDF export") from exc

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, height - margin, "Harvest Report")

    c.setFont("Helvetica", 10)
    c.drawString(margin, height - margin - 20, f"Period: {start_date} - {end_date}")
    c.drawString(
        margin,
        height - margin - 35,
        f"Lot: {lot_name or '-'}  Size: {size_id or '-'}  Rank: {rank_id or '-'}",
    )
    c.drawString(
        margin,
        height - margin - 50,
        f"Records: {record_count}  Total Count: {_format_count(total_count)}",
    )

    chart_height = 250
    chart_top = height - margin - 80
    _draw_bar_chart(
        c,
        items,
        margin,
        chart_top - chart_height,
        width - margin * 2,
        chart_height,
    )

    c.showPage()

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, height - margin, "Summary Table (Daily)")

    y = height - margin - 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "Period")
    c.drawString(margin + 140, y, "Total Count")
    y -= 14

    c.setFont("Helvetica", 10)
    if not items:
        c.drawString(margin, y, "No records.")
    else:
        for item in items:
            if y < margin:
                c.showPage()
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, height - margin, "Summary Table (Daily)")
                y = height - margin - 20
                c.setFont("Helvetica-Bold", 10)
                c.drawString(margin, y, "Period")
                c.drawString(margin + 140, y, "Total Count")
                y -= 14
                c.setFont("Helvetica", 10)
            c.drawString(margin, y, item["period"])
            c.drawRightString(margin + 200, y, _format_count(item["total_count"]))
            y -= 12

    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def _build_target_payload(target, effective_from: date | None) -> dict:
    return {
        "target_type": target.target_type,
        "target_count": target.target_count,
        "effective_from": effective_from,
        "updated_at": target.updated_at,
    }


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
                harvested_at__date=d,
            )
            .order_by("-harvested_at")
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
        harvested_at = timezone.make_aware(
            datetime.combine(d, time.min),
            timezone.get_current_timezone(),
        )

        existing = self._lookup(d, lot, size, rank)
        if existing:
            existing.count = count
            existing.harvested_at = harvested_at
            existing.save(update_fields=["count", "harvested_at"])
            rec = existing
            http_status = status.HTTP_200_OK
        else:
            rec = HarvestRecord.objects.create(
                event_id=None,
                lot_name=lot,
                size=size,
                rank=rank,
                count=count,
                harvested_at=harvested_at,
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
            "harvested_at": "harvested_at",
            # backward-compatible aliases
            "occurred_at": "harvested_at",
            "created_at": "harvested_at",
        }

        qs = HarvestRecord.objects.filter(event_id__isnull=True, harvested_at__date=d).select_related("size", "rank")
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
                new_date = rec.harvested_at.astimezone(timezone.get_current_timezone()).date()
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
            harvested_at = timezone.make_aware(
                datetime.combine(new_date, time.min),
                timezone.get_current_timezone(),
            )

            conflict = (
                HarvestRecord.objects.filter(
                    event_id__isnull=True,
                    lot_name=new_lot,
                    size=size,
                    rank=rank,
                    harvested_at__date=new_date,
                )
                .exclude(id=rec.id)
                .order_by("-harvested_at")
                .first()
            )

            if conflict:
                conflict.count = count
                conflict.harvested_at = harvested_at
                conflict.save(update_fields=["count", "harvested_at"])
                rec.delete()
                rec = conflict
            else:
                rec.lot_name = new_lot
                rec.size = size
                rec.rank = rank
                rec.count = count
                rec.harvested_at = harvested_at
                rec.save(update_fields=["lot_name", "size", "rank", "count", "harvested_at"])

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

        harvested_at = timezone.make_aware(
            datetime.combine(d, time.min),
            timezone.get_current_timezone(),
        )
        rec.count = count
        rec.harvested_at = harvested_at
        rec.save(update_fields=["count", "harvested_at"])

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


class RetrieveHarvestDailyLotView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request, lot_name: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_lot(period_type="daily", lot_name=lot_name)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class RetrieveHarvestWeeklyLotView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request, lot_name: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_lot(period_type="weekly", lot_name=lot_name)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class RetrieveHarvestMonthlyLotView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request, lot_name: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_lot(period_type="monthly", lot_name=lot_name)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class RetrieveHarvestDailyRankView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request, rank_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_rank(period_type="daily", rank_id=rank_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class RetrieveHarvestWeeklyRankView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request, rank_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_rank(period_type="weekly", rank_id=rank_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class RetrieveHarvestMonthlyRankView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request, rank_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_rank(period_type="monthly", rank_id=rank_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class RetrieveHarvestDailySizeRankView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request, size_id: str, rank_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_size_rank(period_type="daily", size_id=size_id, rank_id=rank_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class RetrieveHarvestWeeklySizeRankView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request, size_id: str, rank_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_size_rank(period_type="weekly", size_id=size_id, rank_id=rank_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class RetrieveHarvestMonthlySizeRankView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request, size_id: str, rank_id: str):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_aggregate_by_size_rank(period_type="monthly", size_id=size_id, rank_id=rank_id)
        payload = paginate_list(items, page, page_size)
        return Response(success_response(request, payload))


class UpdateHarvestTargetDailyView(APIView):
    permission_classes = [RoleAdminOnly]

    def put(self, request):
        s = UpdateHarvestTargetRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        target = services.upsert_target("daily", s.validated_data["target_count"])
        payload = _build_target_payload(target, s.validated_data.get("effective_from"))
        return Response(success_response(request, payload), status=status.HTTP_200_OK)


class UpdateHarvestTargetWeeklyView(APIView):
    permission_classes = [RoleAdminOnly]

    def put(self, request):
        s = UpdateHarvestTargetRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        target = services.upsert_target("weekly", s.validated_data["target_count"])
        payload = _build_target_payload(target, s.validated_data.get("effective_from"))
        return Response(success_response(request, payload), status=status.HTTP_200_OK)


class UpdateHarvestTargetMonthlyView(APIView):
    permission_classes = [RoleAdminOnly]

    def put(self, request):
        s = UpdateHarvestTargetRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        target = services.upsert_target("monthly", s.validated_data["target_count"])
        payload = _build_target_payload(target, s.validated_data.get("effective_from"))
        return Response(success_response(request, payload), status=status.HTTP_200_OK)


class ExportHarvestRecordsCsvView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request):
        start_date = _require_query_date(request, "start_date")
        end_date = _require_query_date(request, "end_date")
        if start_date > end_date:
            raise ValidationError({"end_date": "must be >= start_date"})

        lot_name = _get_optional_query_param(request, "lot")
        size_id = _get_optional_query_param(request, "size")
        rank_id = _get_optional_query_param(request, "rank")

        if size_id:
            _require_size(size_id)
        if rank_id:
            _require_rank(rank_id)

        qs = _filter_harvest_records(
            start_date,
            end_date,
            lot_name=lot_name,
            size_id=size_id,
            rank_id=rank_id,
        ).order_by("harvested_at", "id")

        output = StringIO(newline="")
        writer = csv.writer(output)
        writer.writerow(
            [
                "id",
                "event_id",
                "lot_name",
                "size_id",
                "rank_id",
                "count",
                "harvested_at",
            ]
        )

        for rec in qs.iterator():
            writer.writerow(
                [
                    str(rec.id),
                    str(rec.event_id) if rec.event_id else "",
                    rec.lot_name,
                    rec.size_id,
                    rec.rank_id,
                    _format_count(Decimal(rec.count)),
                    timezone.localtime(rec.harvested_at).isoformat(),
                ]
            )

        filename = f"harvest_records_{start_date.isoformat()}_{end_date.isoformat()}.csv"
        content = output.getvalue().encode("utf-8-sig")
        response = HttpResponse(content, content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class ExportHarvestReportPdfView(APIView):
    permission_classes = [RoleAtLeastUser]

    def get(self, request):
        start_date = _require_query_date(request, "start_date")
        end_date = _require_query_date(request, "end_date")
        if start_date > end_date:
            raise ValidationError({"end_date": "must be >= start_date"})

        lot_name = _get_optional_query_param(request, "lot")
        size_id = _get_optional_query_param(request, "size")
        rank_id = _get_optional_query_param(request, "rank")

        if size_id:
            _require_size(size_id)
        if rank_id:
            _require_rank(rank_id)

        qs = _filter_harvest_records(
            start_date,
            end_date,
            lot_name=lot_name,
            size_id=size_id,
            rank_id=rank_id,
        ).order_by("harvested_at", "id")

        items, record_count, total_count = _summarize_records_daily(qs)
        pdf_bytes = _render_harvest_pdf(
            items,
            start_date=start_date,
            end_date=end_date,
            lot_name=lot_name,
            size_id=size_id,
            rank_id=rank_id,
            record_count=record_count,
            total_count=total_count,
        )

        filename = f"harvest_report_{start_date.isoformat()}_{end_date.isoformat()}.pdf"
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
