from __future__ import annotations

import csv
from decimal import Decimal
from datetime import datetime
from io import StringIO
from uuid import uuid4

import pytest
from django.utils import timezone

from apps.harvest.models import HarvestRecord, Rank, Size

pytestmark = pytest.mark.django_db


def _make_record(*, lot_name: str, occurred_at: datetime, count: Decimal) -> HarvestRecord:
    size = Size.objects.get(size_id="S")
    rank = Rank.objects.get(rank_id="A")
    return HarvestRecord.objects.create(
        event_id=uuid4(),
        lot_name=lot_name,
        size=size,
        rank=rank,
        count=count,
        occurred_at=occurred_at,
    )


def test_export_harvest_records_csv_filters_and_headers(user_client):
    occurred_at = timezone.make_aware(datetime(2025, 1, 5, 10, 0, 0))
    _make_record(lot_name="1a", occurred_at=occurred_at, count=Decimal("1.2"))
    _make_record(lot_name="1b", occurred_at=occurred_at, count=Decimal("2.4"))

    resp = user_client.get(
        "/harvest/records/export/csv?start_date=2025-01-01&end_date=2025-01-31&lot=1a"
    )
    assert resp.status_code == 200
    assert resp["Content-Type"].startswith("text/csv")

    content = resp.content.decode("utf-8-sig")
    rows = list(csv.reader(StringIO(content)))

    assert rows[0] == [
        "id",
        "event_id",
        "lot_name",
        "size_id",
        "rank_id",
        "count",
        "occurred_at",
        "created_at",
    ]
    assert len(rows) == 2
    assert rows[1][2] == "1a"
    assert rows[1][5] == "1.2"


def test_export_harvest_report_pdf_returns_pdf(user_client):
    occurred_at = timezone.make_aware(datetime(2025, 1, 10, 9, 30, 0))
    _make_record(lot_name="1a", occurred_at=occurred_at, count=Decimal("3.0"))

    resp = user_client.get(
        "/harvest/records/report/pdf?start_date=2025-01-01&end_date=2025-01-31"
    )
    assert resp.status_code == 200
    assert resp["Content-Type"] == "application/pdf"
    assert resp.content.startswith(b"%PDF-")
