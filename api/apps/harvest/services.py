from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound, ValidationError  # type: ignore

from apps.common.errors import ConflictError
from apps.prices.models import PriceRecord

from .models import HarvestAggregateOverride, HarvestRecord

PERIOD_DAILY = "daily"
PERIOD_WEEKLY = "weekly"
PERIOD_MONTHLY = "monthly"


def _require_defined_category(category_id: str) -> None:
    """Raise NotFound if the category is not registered in prices."""

    if not PriceRecord.objects.filter(category_id=category_id).exists():
        raise NotFound(detail={"category_id": "category not found"})


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
    device_id: Optional[str] = None,
    category_id: Optional[str] = None,
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
        device_id = data.get("device_id")
        category_id = data.get("category_id")
        count = data.get("count")
        occurred_at = data.get("occurred_at")

    if event_id is None:
        raise ValidationError({"event_id": "required"})
    if device_id is None:
        raise ValidationError({"device_id": "required"})
    if category_id is None:
        raise ValidationError({"category_id": "required"})
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

    if HarvestRecord.objects.filter(event_id=event_id).exists():
        # handled as HTTP 409 by custom exception handler
        raise ConflictError("Duplicate event_id")

    return HarvestRecord.objects.create(
        event_id=event_id,
        device_id=device_id,
        category_id=category_id,
        count=count,
        occurred_at=occurred_at,
    )


def _bucket_records(
    period_type: str,
    *,
    category_id: Optional[str] = None,
) -> Dict[Tuple[str, str], Dict[str, Any]]:
    qs = HarvestRecord.objects.all().only("occurred_at", "category_id", "category_name", "count")
    if category_id is not None:
        qs = qs.filter(category_id=category_id)

    bucket: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for rec in qs.iterator():
        period = _period_of(rec.occurred_at, period_type)
        key = (period, rec.category_id)
        if key not in bucket:
            bucket[key] = {
                "period": period,
                "category_id": rec.category_id,
                "category_name": rec.category_name,
                "total_count": 0,
            }
        bucket[key]["total_count"] += int(rec.count)
        if not bucket[key]["category_name"] and rec.category_name:
            bucket[key]["category_name"] = rec.category_name

    # Apply overrides (override wins)
    ov_qs = HarvestAggregateOverride.objects.filter(period_type=period_type).only(
        "period", "category_id", "total_count"
    )
    if category_id is not None:
        ov_qs = ov_qs.filter(category_id=category_id)

    for ov in ov_qs.iterator():
        key = (ov.period, ov.category_id)
        existing_name = bucket.get(key, {}).get("category_name")
        bucket[key] = {
            "period": ov.period,
            "category_id": ov.category_id,
            "category_name": existing_name,
            "total_count": int(ov.total_count),
        }

    return bucket


def list_aggregate(period_type: str) -> List[Dict[str, Any]]:
    bucket = _bucket_records(period_type)
    keys = sorted(bucket.keys(), reverse=True)
    return [bucket[k] for k in keys]


def list_aggregate_by_category(period_type: str, category_id: str) -> List[Dict[str, Any]]:
    _require_defined_category(category_id)

    bucket = _bucket_records(period_type, category_id=category_id)
    keys = sorted(bucket.keys(), reverse=True)
    return [bucket[k] for k in keys]


@transaction.atomic
def upsert_override(period_type: str, category_id: str, period: str, total_count: int) -> HarvestAggregateOverride:
    _require_defined_category(category_id)

    if not isinstance(total_count, int) or isinstance(total_count, bool):
        raise ValidationError({"total_count": "must be an integer"})
    if total_count < 0:
        raise ValidationError({"total_count": "must be >= 0"})

    obj, _ = HarvestAggregateOverride.objects.update_or_create(
        period_type=period_type,
        category_id=category_id,
        period=period,
        defaults={"total_count": total_count},
    )
    return obj
