from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from apps.harvest.models import HarvestRecord


pytestmark = pytest.mark.django_db


def _payload(resp):
    if hasattr(resp, "data"):
        return resp.data
    return resp.json()


def test_system_tablet_harvest_register(user_client):
    html_path_candidates = [
        Path(__file__).resolve().parents[2] / "harvest_register.html",  # repo root (local host)
        Path(__file__).resolve().parents[1] / "harvest_register.html",  # mounted root (docker)
        Path("/harvest_register.html"),  # file mount (docker)
    ]
    html_path = next((p for p in html_path_candidates if p.exists()), None)
    if html_path:
        html = html_path.read_text(encoding="utf-8")
        assert "/tablet/harvest/" in html
        assert "Math.round(entry.kg * 1000)" in html

    date_str = "2025-01-15"
    d = date.fromisoformat(date_str)

    entries = [
        {"lot": "1e", "size": "L", "rank": "A", "count": 1500},
        {"lot": "1e", "size": "SS", "rank": "B", "count": 250},
        {"lot": "2e", "size": "黒", "rank": "C", "count": 100},
        {"lot": "2e", "size": "小", "rank": "小", "count": 0},
    ]

    for entry in entries:
        resp = user_client.post(
            f"/tablet/harvest/{date_str}?lot={entry['lot']}&size={entry['size']}&rank={entry['rank']}",
            {"count": entry["count"]},
            format="json",
        )
        assert resp.status_code in (200, 201), _payload(resp)

    qs = HarvestRecord.objects.filter(event_id__isnull=True, occurred_at__date=d)
    assert qs.count() == len(entries)

    for entry in entries:
        rec = HarvestRecord.objects.get(
            event_id__isnull=True,
            lot_name=entry["lot"],
            size_id=entry["size"],
            rank_id=entry["rank"],
            occurred_at__date=d,
        )
        assert rec.count == entry["count"]

    total = sum(entry["count"] for entry in entries)
    resp = user_client.get("/harvest/amount/daily?page=1&page_size=50")
    assert resp.status_code == 200, _payload(resp)
    items = _payload(resp)["data"]["items"]
    hit = [item for item in items if item.get("period") == date_str]
    assert hit and hit[0]["total_count"] == total
