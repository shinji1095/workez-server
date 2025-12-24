import uuid
import pytest
from datetime import date
from django.utils import timezone  # type: ignore

from apps.harvest.models import HarvestAggregateOverride


pytestmark = pytest.mark.django_db


def _payload(resp):
    if hasattr(resp, "data"):
        return resp.data
    return resp.json()


def _prepare_price(admin_client, category_id: str, unit_price_yen: int = 100, effective_from: str = "2025-01-01"):
    resp = admin_client.post(
        f"/prices/category/{category_id}",
        {"unit_price_yen": unit_price_yen, "effective_from": effective_from},
        format="json",
    )
    assert resp.status_code in (200, 201), _payload(resp)


def test_weekly_override_period_is_determined_by_date_param(admin_client, device_client, user_client):
    _prepare_price(admin_client, "C1")

    # Arrange: add at least one record so weekly list is non-empty
    occurred_at = timezone.now().isoformat()
    device_client.post(
        "/harvest/amount/add",
        {
            "event_id": str(uuid.uuid4()),
            "device_id": "D1",
            "category_id": "C1",
            "count": 3,
            "occurred_at": occurred_at,
        },
        format="json",
    )

    # Act: patch weekly override using date=YYYY-MM-DD
    d = date(2025, 1, 5)  # deterministic
    iso = d.isocalendar()
    expected_period = f"{iso.year}-W{iso.week:02d}"

    resp = admin_client.patch(
        f"/harvest/amount/weekly/category/C1?date={d.isoformat()}",
        {"total_count": 99},
        format="json",
    )
    assert resp.status_code == 200

    # Assert: DB override period is computed from the date param
    ov = HarvestAggregateOverride.objects.get(period_type="weekly", category_id="C1", period=expected_period)
    assert ov.total_count == 99

    # And: weekly-by-category API reflects the override for that period
    resp2 = user_client.get("/harvest/amount/weekly/category/C1?page=1&page_size=50")
    assert resp2.status_code == 200
    data = resp2.json()["data"]["items"]
    # Find the overridden period entry
    hit = [i for i in data if i.get("period") == expected_period]
    assert hit and hit[0]["total_count"] == 99
