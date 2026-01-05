from __future__ import annotations

import pytest

from apps.harvest.models import HarvestRecord


pytestmark = pytest.mark.django_db


def _payload(resp):
    if hasattr(resp, "data"):
        return resp.data
    return resp.json()


def _assert_success_envelope(resp):
    body = _payload(resp)
    assert isinstance(body, dict)
    assert "data" in body
    return body["data"]


def test_tablet_harvest_list_edit_delete(user_client):
    date_str = "2025-01-15"
    entries = [
        {"lot": "1e", "size": "L", "rank": "A", "count": 1500},
        {"lot": "1e", "size": "SS", "rank": "B", "count": 250},
        {"lot": "2e", "size": "黒", "rank": "C", "count": 100},
    ]

    for entry in entries:
        resp = user_client.post(
            f"/tablet/harvest/{date_str}?lot={entry['lot']}&size={entry['size']}&rank={entry['rank']}",
            {"count": entry["count"]},
            format="json",
        )
        assert resp.status_code in (200, 201), _payload(resp)

    # Single-record retrieval (backward compatible)
    resp = user_client.get(f"/tablet/harvest/{date_str}?lot=1e&size=L&rank=A")
    assert resp.status_code == 200, _payload(resp)
    single = _assert_success_envelope(resp)
    assert single["count"] == 1500

    # List retrieval (no size/rank) + pagination
    resp = user_client.get(f"/tablet/harvest/{date_str}?page=1&page_size=2&sort=lot&order=asc")
    assert resp.status_code == 200, _payload(resp)
    data = _assert_success_envelope(resp)
    assert data["total"] == len(entries)
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) == 2
    first = data["items"][0]
    for k in ("id", "lot_name", "size_id", "rank_id", "count", "occurred_at", "created_at"):
        assert k in first

    # List retrieval with lot filter
    resp = user_client.get(f"/tablet/harvest/{date_str}?page=1&page_size=50&lot=1e")
    assert resp.status_code == 200, _payload(resp)
    filtered = _assert_success_envelope(resp)
    assert filtered["total"] == 2

    # Update by id (edit fields)
    record_id = first["id"]
    resp = user_client.put(
        f"/tablet/harvest/{date_str}?id={record_id}",
        {"date": date_str, "lot": "9e", "size": "L", "rank": "B", "count": 1234},
        format="json",
    )
    assert resp.status_code == 200, _payload(resp)
    updated = _assert_success_envelope(resp)
    assert updated["id"] == record_id
    assert updated["lot_name"] == "9e"
    assert updated["size_id"] == "L"
    assert updated["rank_id"] == "B"
    assert updated["count"] == 1234
    assert HarvestRecord.objects.filter(id=record_id, lot_name="9e", count=1234).exists()

    # Delete by id
    resp = user_client.delete(f"/tablet/harvest/{date_str}?id={record_id}")
    assert resp.status_code == 200, _payload(resp)
    deleted = _assert_success_envelope(resp)
    assert deleted["deleted"] is True
    assert deleted["id"] == record_id
    assert not HarvestRecord.objects.filter(id=record_id).exists()

