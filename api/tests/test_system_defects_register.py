from __future__ import annotations

from decimal import Decimal
from pathlib import Path
import uuid

import pytest

from apps.defects.models import DefectsRecord


pytestmark = pytest.mark.django_db


def _payload(resp):
    if hasattr(resp, "data"):
        return resp.data
    return resp.json()


def test_system_defects_register(device_client):
    html_path_candidates = [
        Path(__file__).resolve().parents[2] / "defects_register.html",  # repo root (local host)
        Path(__file__).resolve().parents[1] / "defects_register.html",  # mounted root (docker)
        Path("/defects_register.html"),  # file mount (docker)
    ]
    html_path = next((p for p in html_path_candidates if p.exists()), None)
    if html_path:
        html = html_path.read_text(encoding="utf-8")
        assert "/defects/amount/add" in html
        assert "event_id" in html

    entries = [
        {"event_id": uuid.uuid4(), "count": Decimal("1.5")},
        {"event_id": uuid.uuid4(), "count": Decimal("0.5")},
    ]

    for entry in entries:
        resp = device_client.post(
            "/defects/amount/add",
            {"event_id": entry["event_id"], "count": entry["count"]},
            format="json",
        )
        assert resp.status_code == 201, _payload(resp)

    assert DefectsRecord.objects.count() == len(entries)

    for entry in entries:
        rec = DefectsRecord.objects.get(event_id=entry["event_id"])
        assert rec.count == entry["count"]

