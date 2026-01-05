from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound, ValidationError  # type: ignore

from apps.common.errors import ConflictError

from .models import HarvestAggregateOverride, HarvestRecord, Rank, Size

PERIOD_DAILY = "daily"
PERIOD_WEEKLY = "weekly"
PERIOD_MONTHLY = "monthly"


def _require_defined_size(size_id: str) -> Size:
    """Raise NotFound if size_id is not registered in sizes master."""

    size = Size.objects.filter(size_id=size_id).first()
    if not size:
        raise NotFound(detail={"size_id": "size not found"})
    return size


def _normalize_occurred_at(dt: datetime) -> datetime:
    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def _period_of(dt: datetime, period_type: str) -> str:
    dt = _normalize_occurred_at(dt)
    d = timezone.localtime(dt).date()

    if period_type == PERIOD_DAILY:
        return d.isoformat()

    if period_type == PERIOD_WEEKLY:
        y, w, _ = d.isocalendar()
        return f"{y}-W{w:02d}"

    if period_type == PERIOD_MONTHLY:
        return f"{d.year}-{d.month:02d}"

    raise ValidationError({"period_type": "invalid"})


@transaction.atomic
def add_record(
    data: Optional[Dict[str, Any]] = None,
    *,
    event_id=None,
    lot_name: Optional[str] = None,
    size: Optional[Size] = None,
    size_id: Optional[str] = None,
    rank: Optional[Rank] = None,
    rank_id: Optional[str] = None,
    count: Optional[int] = None,
    occurred_at: Optional[datetime] = None,
) -> HarvestRecord:
    """Create a HarvestRecord.

    Compatibility note:
    - tests/services sometimes call add_record({...}) (positional dict)
    - API code often calls add_record(**validated_data)
    """

    if data is not None:
        if not isinstance(data, dict):
            raise ValidationError({"data": "must be an object"})
        event_id = data.get("event_id")
        lot_name = data.get("lot_name")
        size = data.get("size")
        size_id = data.get("size_id")
        rank = data.get("rank")
        rank_id = data.get("rank_id")
        count = data.get("count")
        occurred_at = data.get("occurred_at")

    if event_id is None:
        raise ValidationError({"event_id": "required"})
    if lot_name is None:
        raise ValidationError({"lot_name": "required"})
    if size is None and size_id is None:
        raise ValidationError({"size_id": "required"})
    if rank is None and rank_id is None:
        raise ValidationError({"rank_id": "required"})
    if count is None:
        raise ValidationError({"count": "required"})
    if occurred_at is None:
        raise ValidationError({"occurred_at": "required"})

    # type strictness is handled in serializers for API requests.
    if not isinstance(count, int) or isinstance(count, bool):
        raise ValidationError({"count": "must be an integer"})
    if count <= 0:
        raise ValidationError({"count": "must be >= 1"})

    if isinstance(occurred_at, str):
        # allow ISO strings in service layer for tests/tools
        from django.utils.dateparse import parse_datetime

        parsed = parse_datetime(occurred_at)
        if parsed is None:
            raise ValidationError({"occurred_at": "invalid datetime"})
        occurred_at = parsed

    if not isinstance(occurred_at, datetime):
        raise ValidationError({"occurred_at": "invalid datetime"})

    occurred_at = _normalize_occurred_at(occurred_at)

    if size is None:
        size = Size.objects.filter(size_id=size_id).first()
        if size is None:
            raise NotFound(detail={"size_id": "size not found"})

    if rank is None:
        rank = Rank.objects.filter(rank_id=rank_id).first()
        if rank is None:
            raise NotFound(detail={"rank_id": "rank not found"})

    if HarvestRecord.objects.filter(event_id=event_id).exists():
        # handled as HTTP 409 by custom exception handler
        raise ConflictError("Duplicate event_id")

    return HarvestRecord.objects.create(
        event_id=event_id,
        lot_name=lot_name,
        size=size,
        rank=rank,
        count=count,
        occurred_at=occurred_at,
    )


def _bucket_records(
    period_type: str,
    *,
    size_id: Optional[str] = None,
) -> Dict[Tuple[str, str], Dict[str, Any]]:
    qs = HarvestRecord.objects.all().only("occurred_at", "size", "count")
    size: Optional[Size] = None
    if size_id is not None:
        size = _require_defined_size(size_id)
        qs = qs.filter(size_id=size_id)

    bucket: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for rec in qs.iterator():
        period = _period_of(rec.occurred_at, period_type)
        key = (period, rec.size_id)
        if key not in bucket:
            bucket[key] = {
                "period": period,
                "size_id": rec.size_id,
                "size_name": size.size_name if size else None,
                "total_count": 0,
            }
        bucket[key]["total_count"] += int(rec.count)

    # Apply overrides (override wins)
    ov_qs = HarvestAggregateOverride.objects.filter(period_type=period_type).only("period", "size", "total_count")
    if size_id is not None:
        ov_qs = ov_qs.filter(size_id=size_id)

    for ov in ov_qs.iterator():
        key = (ov.period, ov.size_id)
        bucket[key] = {
            "period": ov.period,
            "size_id": ov.size_id,
            "size_name": size.size_name if size else None,
            "total_count": int(ov.total_count),
        }

    return bucket


def list_aggregate_total(period_type: str) -> List[Dict[str, Any]]:
    qs = HarvestRecord.objects.all().only("occurred_at", "count")
    bucket: Dict[str, int] = defaultdict(int)
    for rec in qs.iterator():
        period = _period_of(rec.occurred_at, period_type)
        bucket[period] += int(rec.count)

    items = [{"period": period, "total_count": total} for period, total in bucket.items()]
    items.sort(key=lambda x: x["period"], reverse=True)
    return items


def list_aggregate_by_size(period_type: str, size_id: str) -> List[Dict[str, Any]]:
    bucket = _bucket_records(period_type, size_id=size_id)
    keys = sorted(bucket.keys(), reverse=True)
    return [bucket[k] for k in keys]


@transaction.atomic
def upsert_override(period_type: str, size_id: str, period: str, total_count: int) -> HarvestAggregateOverride:
    size = _require_defined_size(size_id)

    if not isinstance(total_count, int) or isinstance(total_count, bool):
        raise ValidationError({"total_count": "must be an integer"})
    if total_count < 0:
        raise ValidationError({"total_count": "must be >= 0"})

    obj, _ = HarvestAggregateOverride.objects.update_or_create(
        period_type=period_type,
        size=size,
        period=period,
        defaults={"size_name": size.size_name, "total_count": total_count},
    )
    return obj
