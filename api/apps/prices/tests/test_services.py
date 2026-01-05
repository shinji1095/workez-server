import pytest
from apps.prices import services

pytestmark = pytest.mark.django_db

def test_create_price_and_list_monthly():
    services.create_price(
        "S",
        "A",
        {
            "year": 2025,
            "month": 1,
            "unit_price_yen": 100,
        },
    )
    items = services.list_monthly()
    assert items[0]["unit_price_yen"] == 100
