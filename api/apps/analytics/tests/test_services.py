import pytest
from datetime import date
import uuid
from django.utils import timezone
from apps.harvest import services as harvest_services
from apps.prices import services as price_services
from apps.analytics import services as analytics_services

pytestmark = pytest.mark.django_db

def test_revenue_monthly_basic():
    # price
    price_services.create_price("C1", {
        "unit_price_yen": 100,
        "effective_from": date(2025, 1, 1),
    })
    # harvest
    harvest_services.add_record({
        "device_id": "DEV001",
        "category_id": "C1",
        "count": 10,
        "event_id": str(uuid.uuid4()),
            "occurred_at": timezone.now().replace(year=2025, month=1, day=15),
    })
    items = analytics_services.list_revenue_monthly()
    assert items[0]["revenue_yen"] == 1000
