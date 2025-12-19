from __future__ import annotations
from typing import Any, Dict, List
from collections import defaultdict
from datetime import datetime
from django.db import transaction  # type: ignore
from django.utils import timezone  # type: ignore

from .models import DefectsRecord
from apps.harvest.models import HarvestRecord

def _period_weekly(dt: datetime) -> str:
    iso = dt.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"

def _period_monthly(dt: datetime) -> str:
    return f"{dt.year:04d}-{dt.month:02d}"

@transaction.atomic
def add_record(data: Dict[str, Any]) -> DefectsRecord:
    occurred_at = data.get("occurred_at") or timezone.now()
    rec = DefectsRecord.objects.create(
        device_id=data["device_id"],
        count=data["count"],
        occurred_at=occurred_at,
    )
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
    # defects
    defects = list_amount(period_type)
    d_map = {i["period"]: i["total_defects"] for i in defects}

    # harvest totals
    h_bucket = defaultdict(int)
    for r in HarvestRecord.objects.all().iterator():
        p = _period_weekly(r.occurred_at) if period_type == "weekly" else _period_monthly(r.occurred_at)
        h_bucket[p] += int(r.count)
    items = []
    for p in sorted(set(d_map.keys()) | set(h_bucket.keys()), reverse=True):
        total_defects = int(d_map.get(p, 0))
        total_harvest = int(h_bucket.get(p, 0))
        ratio = (total_defects / total_harvest * 100.0) if total_harvest > 0 else 0.0
        items.append({
            "period": p,
            "defects_ratio_percent": round(ratio, 3),
            "total_defects": total_defects,
            "total_harvest": total_harvest,
        })
    return items
