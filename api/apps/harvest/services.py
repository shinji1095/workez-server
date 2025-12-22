from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from django.db import IntegrityError, transaction  # type: ignore
from django.utils import timezone  # type: ignore
from rest_framework.exceptions import ValidationError  # type: ignore

from apps.common.errors import ConflictError
from .models import HarvestAggregateOverride, HarvestRecord, HarvestTarget


def _period_daily(dt: datetime) -> str:
    return dt.date().isoformat()


def _period_weekly(dt: datetime) -> str:
    iso = dt.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _period_monthly(dt: datetime) -> str:
    return f"{dt.year:04d}-{dt.month:02d}"


@transaction.atomic
def add_record(data: Dict[str, Any]) -> HarvestRecord:
    event_id = data.get("event_id")
    if not event_id:
        raise ValidationError({"event_id": ["This field is required."]})

    if HarvestRecord.objects.filter(event_id=event_id).exists():
        raise ConflictError({"event_id": ["duplicate event_id"]})

    try:
        rec = HarvestRecord.objects.create(
            event_id=event_id,
            device_id=data["device_id"],
            category_id=data["category_id"],
            category_name=data.get("category_name"),
            count=data["count"],
            occurred_at=data.get("occurred_at") or timezone.now(),
        )
    except IntegrityError as e:
        # Race condition safety: if unique constraint triggered on event_id, convert to 409.
        if "event_id" in str(e).lower():
            raise ConflictError({"event_id": ["duplicate event_id"]}) from e
        raise

    return rec


def _aggregate_records(period_type: str, category_id: Optional[str] = None) -> List[Dict[str, Any]]:
    qs = HarvestRecord.objects.all()
    if category_id is not None:
        qs = qs.filter(category_id=category_id)

    bucket_total: Dict[str, int] = defaultdict(int)
    bucket_cat: Dict[Tuple[str, str, Optional[str]], int] = defaultdict(int)

    for r in qs.iterator():
        if period_type == "daily":
            p = _period_daily(r.occurred_at)
        elif period_type == "weekly":
            p = _period_weekly(r.occurred_at)
        else:
            p = _period_monthly(r.occurred_at)

        bucket_total[p] += int(r.count)
        cid = r.category_id or ""
        bucket_cat[(p, cid, r.category_name)] += int(r.count)

    if category_id is None:
        items = [{"period": p, "total_count": c} for p, c in bucket_total.items()]
        items.sort(key=lambda x: x["period"], reverse=True)
        return items

    items: List[Dict[str, Any]] = []
    for (p, cid, cname), c in bucket_cat.items():
        items.append(
            {
                "period": p,
                "category_id": cid,
                "category_name": cname,
                "total_count": c,
            }
        )
    items.sort(key=lambda x: (x["period"], x["category_id"]), reverse=True)
    return items


def list_aggregate(period_type: str) -> List[Dict[str, Any]]:
    return _aggregate_records(period_type, category_id=None)


def list_aggregate_by_category(period_type: str, category_id: str) -> List[Dict[str, Any]]:
    raw = _aggregate_records(period_type, category_id=category_id)

    overrides = list(
        HarvestAggregateOverride.objects.filter(period_type=period_type, category_id=category_id)
    )
    ov_map = {o.period: o for o in overrides}

    raw_periods = set()
    for item in raw:
        p = item.get("period")
        if not p:
            continue
        raw_periods.add(p)
        ov = ov_map.get(p)
        if ov:
            item["total_count"] = ov.total_count
            if ov.category_name is not None:
                item["category_name"] = ov.category_name

    # Add override-only periods so that the list reflects overrides even when no raw record exists.
    for ov in overrides:
        if ov.period in raw_periods:
            continue
        raw.append(
            {
                "period": ov.period,
                "category_id": ov.category_id,
                "category_name": ov.category_name,
                "total_count": ov.total_count,
            }
        )

    raw.sort(key=lambda x: (x.get("period") or "", x.get("category_id") or ""), reverse=True)
    return raw


@transaction.atomic
def patch_override(period_type: str, category_id: str, period: str, total_count: int) -> HarvestAggregateOverride:
    obj, _ = HarvestAggregateOverride.objects.update_or_create(
        period_type=period_type,
        period=period,
        category_id=category_id,
        defaults={"total_count": total_count},
    )
    return obj


@transaction.atomic
def update_target(target_type: str, target_count: int) -> HarvestTarget:
    obj, _ = HarvestTarget.objects.update_or_create(
        target_type=target_type,
        defaults={"target_count": target_count},
    )
    return obj


def get_target(target_type: str) -> Optional[HarvestTarget]:
    try:
        return HarvestTarget.objects.get(target_type=target_type)
    except HarvestTarget.DoesNotExist:
        return None
