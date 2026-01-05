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
