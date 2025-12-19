import pytest
from django.utils import timezone
from apps.defects import services

pytestmark = pytest.mark.django_db

def test_add_record_and_list_weekly():
    services.add_record({"device_id": "DEV001", "count": 3, "occurred_at": timezone.now()})
    items = services.list_amount("weekly")
    assert items[0]["total_defects"] == 3
