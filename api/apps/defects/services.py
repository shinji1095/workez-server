from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

from django.db import IntegrityError, transaction  # type: ignore
from django.utils import timezone  # type: ignore
from rest_framework.exceptions import ValidationError  # type: ignore

from apps.common.errors import ConflictError
from apps.harvest.models import HarvestRecord
from .models import DefectsRecord


def _period_weekly(dt: datetime) -> str:
    iso = dt.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _period_monthly(dt: datetime) -> str:
    return f"{dt.year:04d}-{dt.month:02d}"


@transaction.atomic
def add_record(data: Dict[str, Any]) -> DefectsRecord:
    event_id = data.get("event_id")
    if not event_id:
        raise ValidationError({"event_id": ["This field is required."]})

    if DefectsRecord.objects.filter(event_id=event_id).exists():
        raise ConflictError({"event_id": ["duplicate event_id"]})

    try:
        rec = DefectsRecord.objects.create(
            event_id=event_id,
            device_id=data["device_id"],
            category_id=data["category_id"],
            count=data["count"],
            occurred_at=data.get("occurred_at") or timezone.now(),
        )
    except IntegrityError as e:
        if "event_id" in str(e).lower():
            raise ConflictError({"event_id": ["duplicate event_id"]}) from e
        raise

    return rec


def list_amount(period_type: str) -> List[Dict[str, Any]]:
    qs = DefectsRecord.objects.all()
    bucket = defaultdict(int)
    for r in qs.iterator():
        p = _period_weekly(r.occurred_at) if period_type == "weekly" else _period_monthly(r.occurred_at)
        bucket[p] += int(r.count)
    items = [{"period": p, "total_defects": c} for p, c in bucket.items()]
    items.sort(key=lambda x: x["period"], reverse=True)
    return items


def list_ratio(period_type: str) -> List[Dict[str, Any]]:
    defects = list_amount(period_type)
    d_map = {i["period"]: i["total_defects"] for i in defects}

    h_bucket = defaultdict(int)
    for r in HarvestRecord.objects.all().iterator():
        p = _period_weekly(r.occurred_at) if period_type == "weekly" else _period_monthly(r.occurred_at)
        h_bucket[p] += int(r.count)

    items = []
    for p in sorted(set(d_map.keys()) | set(h_bucket.keys()), reverse=True):
        total_defects = int(d_map.get(p, 0))
        total_harvest = int(h_bucket.get(p, 0))
        ratio = (total_defects / total_harvest * 100.0) if total_harvest > 0 else 0.0
        items.append(
            {
                "period": p,
                "defects_ratio_percent": round(ratio, 3),
                "total_defects": total_defects,
                "total_harvest": total_harvest,
            }
        )
    return items
