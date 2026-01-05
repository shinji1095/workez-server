import pytest
from django.utils import timezone
from apps.defects import services
from apps.common.errors import ConflictError
import uuid

pytestmark = pytest.mark.django_db

def test_add_record_and_list_weekly():
    eid = uuid.uuid4()
    services.add_record({"event_id": eid, "category_id": "C1", "count": 3, "occurred_at": timezone.now()})
    items = services.list_amount("weekly")
    assert items[0]["total_defects"] == 3

    with pytest.raises(ConflictError):
        services.add_record({"event_id": eid, "category_id": "C1", "count": 1, "occurred_at": timezone.now()})
