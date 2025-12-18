import pytest
from datetime import date
from apps.prices import services

pytestmark = pytest.mark.django_db

def test_create_price_and_list_monthly():
    services.create_price("C1", {
        "unit_price_yen": 100,
        "effective_from": date(2025, 1, 1),
    })
    items = services.list_monthly()
    assert items[0]["unit_price_yen"] == 100
