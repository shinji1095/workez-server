import pytest
from django.utils import timezone
from apps.harvest import services
from apps.common.errors import ConflictError
import uuid

pytestmark = pytest.mark.django_db

def test_add_record_and_aggregate_daily():
    eid = uuid.uuid4()
    services.add_record({
        "event_id": eid,
        "lot_name": "1e",
        "size_id": "S",
        "rank_id": "A",
        "count": 10,
        "occurred_at": timezone.now(),
    })
    items = services.list_aggregate_total("daily")
    assert items[0]["total_count"] == 10

    with pytest.raises(ConflictError):
        services.add_record({
            "event_id": eid,
            "lot_name": "1e",
            "size_id": "S",
            "rank_id": "A",
            "count": 1,
            "occurred_at": timezone.now(),
        })


def test_list_aggregate_by_lot_daily_filters():
    now = timezone.now()
    services.add_record({
        "event_id": uuid.uuid4(),
        "lot_name": "1e",
        "size_id": "S",
        "rank_id": "A",
        "count": 3,
        "occurred_at": now,
    })
    services.add_record({
        "event_id": uuid.uuid4(),
        "lot_name": "1e",
        "size_id": "S",
        "rank_id": "A",
        "count": 7,
        "occurred_at": now,
    })
    services.add_record({
        "event_id": uuid.uuid4(),
        "lot_name": "2a",
        "size_id": "S",
        "rank_id": "A",
        "count": 5,
        "occurred_at": now,
    })

    items = services.list_aggregate_by_lot("daily", "1e")
    assert items
    assert all(item["lot_name"] == "1e" for item in items)
    assert sum(item["total_count"] for item in items) == 10
