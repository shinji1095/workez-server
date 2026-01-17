from __future__ import annotations
from typing import Dict, Any, List, Tuple
from collections import defaultdict
from decimal import Decimal
from datetime import date, datetime, timedelta

from apps.harvest.models import HarvestRecord
from apps.prices.models import PriceRecord

def _period_monthly(dt: datetime) -> str:
    return f"{dt.year:04d}-{dt.month:02d}"

def _period_yearly(dt: datetime) -> str:
    return f"{dt.year:04d}"

def _price_lookup_table() -> Dict[Tuple[str, str], List[PriceRecord]]:
    table: Dict[Tuple[str, str], List[PriceRecord]] = defaultdict(list)
    for p in PriceRecord.objects.all().order_by("size_id", "rank_id", "effective_from"):
        table[(p.size_id, p.rank_id)].append(p)
    return table

def _find_price(prices: List[PriceRecord], d: date) -> int | None:
    # choose the latest effective_from <= d and effective_to >= d if set
    best = None
    for p in prices:
        if p.effective_from <= d and (p.effective_to is None or p.effective_to >= d):
            best = p
    return best.unit_price_yen if best else None


def _to_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(str(value))
    return Decimal(str(value))

def list_revenue_monthly() -> List[Dict[str, Any]]:
    price_table = _price_lookup_table()
    bucket = defaultdict(Decimal)
    for r in HarvestRecord.objects.all().iterator():
        prices = price_table.get((r.size_id, r.rank_id))
        if not prices:
            continue
        unit = _find_price(prices, r.occurred_at.date())
        if unit is None:
            continue
        p = _period_monthly(r.occurred_at)
        bucket[p] += _to_decimal(r.count) * Decimal(unit)
    items = [{"period": p, "revenue_yen": v} for p, v in bucket.items()]
    items.sort(key=lambda x: x["period"], reverse=True)
    return items

def list_revenue_yearly() -> List[Dict[str, Any]]:
    price_table = _price_lookup_table()
    bucket = defaultdict(Decimal)
    for r in HarvestRecord.objects.all().iterator():
        prices = price_table.get((r.size_id, r.rank_id))
        if not prices:
            continue
        unit = _find_price(prices, r.occurred_at.date())
        if unit is None:
            continue
        p = _period_yearly(r.occurred_at)
        bucket[p] += _to_decimal(r.count) * Decimal(unit)
    items = [{"period": p, "revenue_yen": v} for p, v in bucket.items()]
    items.sort(key=lambda x: x["period"], reverse=True)
    return items

def list_harvest_monthly_forecast(months_ahead: int = 1) -> List[Dict[str, Any]]:
    """Naive forecast: next month predicted = last month actual.

    OpenAPIにはアルゴリズム要件が無いため、暫定のベースライン実装。
    """
    bucket = defaultdict(Decimal)
    for r in HarvestRecord.objects.all().iterator():
        p = _period_monthly(r.occurred_at)
        bucket[p] += _to_decimal(r.count)

    # Determine last month with data
    if not bucket:
        return []
    last_period = sorted(bucket.keys())[-1]
    last_val = bucket[last_period]

    # Compute next period string
    y, m = map(int, last_period.split("-"))
    m += 1
    if m == 13:
        y += 1
        m = 1
    next_period = f"{y:04d}-{m:02d}"

    return [
        {"period": next_period, "predicted_count": last_val},
    ]
