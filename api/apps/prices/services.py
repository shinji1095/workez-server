from __future__ import annotations

import calendar
from datetime import date
from typing import Any, Dict, List, Tuple

from django.db import transaction  # type: ignore
from django.http import Http404  # type: ignore

from apps.harvest.models import Rank, Size

from .models import PriceRecord

def _month_range(year: int, month: int) -> Tuple[date, date]:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)

def _require_size_rank(size_id: str, rank_id: str) -> Tuple[Size, Rank]:
    size = Size.objects.filter(size_id=size_id).first()
    if not size:
        raise Http404()
    rank = Rank.objects.filter(rank_id=rank_id).first()
    if not rank:
        raise Http404()
    return size, rank

@transaction.atomic
def create_price(size_id: str, rank_id: str, data: Dict[str, Any]) -> PriceRecord:
    size, rank = _require_size_rank(size_id, rank_id)
    effective_from, effective_to = _month_range(int(data["year"]), int(data["month"]))

    rec = PriceRecord.objects.create(
        size=size,
        rank=rank,
        unit_price_yen=data["unit_price_yen"],
        effective_from=effective_from,
        effective_to=effective_to,
    )
    return rec

@transaction.atomic
def update_price(size_id: str, rank_id: str, data: Dict[str, Any]) -> PriceRecord:
    _require_size_rank(size_id, rank_id)
    effective_from, effective_to = _month_range(int(data["year"]), int(data["month"]))

    rec = PriceRecord.objects.filter(size_id=size_id, rank_id=rank_id, effective_from=effective_from).first()
    if not rec:
        raise Http404()

    rec.unit_price_yen = data["unit_price_yen"]
    rec.effective_to = effective_to
    rec.save(update_fields=["unit_price_yen", "effective_to", "updated_at"])
    return rec


@transaction.atomic
def delete_price(size_id: str, rank_id: str, *, year: int, month: int) -> int:
    effective_from, _ = _month_range(int(year), int(month))
    qs = PriceRecord.objects.filter(size_id=size_id, rank_id=rank_id, effective_from=effective_from)
    if not qs.exists():
        raise Http404()
    deleted, _ = qs.delete()
    return deleted

def list_monthly() -> List[Dict[str, Any]]:
    items = []
    for rec in PriceRecord.objects.all().only("effective_from", "size_id", "rank_id", "unit_price_yen").iterator():
        period = f"{rec.effective_from.year:04d}-{rec.effective_from.month:02d}"
        items.append({"period": period, "size_id": rec.size_id, "rank_id": rec.rank_id, "unit_price_yen": rec.unit_price_yen})
    items.sort(key=lambda x: (x["period"], x["size_id"], x["rank_id"]), reverse=True)
    return items

def list_yearly() -> List[Dict[str, Any]]:
    bucket: Dict[Tuple[str, str, str], List[int]] = {}
    for rec in PriceRecord.objects.all().only("effective_from", "size_id", "rank_id", "unit_price_yen").iterator():
        period = f"{rec.effective_from.year:04d}"
        key = (period, rec.size_id, rec.rank_id)
        bucket.setdefault(key, []).append(int(rec.unit_price_yen))

    items = []
    for (period, size_id, rank_id), prices in bucket.items():
        avg = int(round(sum(prices) / len(prices))) if prices else 0
        items.append({"period": period, "size_id": size_id, "rank_id": rank_id, "unit_price_yen": avg})

    items.sort(key=lambda x: (x["period"], x["size_id"], x["rank_id"]), reverse=True)
    return items
