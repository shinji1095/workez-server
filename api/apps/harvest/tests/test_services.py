import pytest
from django.utils import timezone
from apps.harvest import services

pytestmark = pytest.mark.django_db

def test_add_record_and_aggregate_daily():
    services.add_record({"device_id": "DEV001", "count": 10, "occurred_at": timezone.now()})
    items = services.list_aggregate("daily")
    assert items[0]["total_count"] == 10
