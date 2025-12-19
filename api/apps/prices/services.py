from __future__ import annotations
from typing import Any, Dict, List
from django.db import transaction  # type: ignore
from django.http import Http404  # type: ignore
from .models import PriceRecord

@transaction.atomic
def create_price(category_id: str, data: Dict[str, Any]) -> PriceRecord:
    rec = PriceRecord.objects.create(
        category_id=category_id,
        category_name=data.get("category_name"),
        unit_price_yen=data["unit_price_yen"],
        effective_from=data["effective_from"],
        effective_to=data.get("effective_to"),
    )
    return rec

def _latest_record(category_id: str) -> PriceRecord:
    rec = PriceRecord.objects.filter(category_id=category_id).order_by("-effective_from").first()
    if not rec:
        raise Http404()
    return rec

@transaction.atomic
def update_price(category_id: str, data: Dict[str, Any]) -> PriceRecord:
    rec = _latest_record(category_id)
    for k in ["category_name", "unit_price_yen", "effective_to"]:
        if k in data:
            setattr(rec, k, data[k])
    rec.save()
    return rec

@transaction.atomic
def delete_price(category_id: str) -> int:
    qs = PriceRecord.objects.filter(category_id=category_id)
    deleted, _ = qs.delete()
    return deleted

def list_monthly() -> List[Dict[str, Any]]:
    items = []
    for rec in PriceRecord.objects.all().iterator():
        period = f"{rec.effective_from.year:04d}-{rec.effective_from.month:02d}"
        items.append({
            "period": period,
            "category_id": rec.category_id,
            "category_name": rec.category_name,
            "unit_price_yen": rec.unit_price_yen,
        })
    items.sort(key=lambda x: (x["period"], x["category_id"]), reverse=True)
    return items

def list_yearly() -> List[Dict[str, Any]]:
    items = []
    for rec in PriceRecord.objects.all().iterator():
        period = f"{rec.effective_from.year:04d}"
        items.append({
            "period": period,
            "category_id": rec.category_id,
            "category_name": rec.category_name,
            "unit_price_yen": rec.unit_price_yen,
        })
    items.sort(key=lambda x: (x["period"], x["category_id"]), reverse=True)
    return items
