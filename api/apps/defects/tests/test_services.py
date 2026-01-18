from decimal import Decimal
import pytest
from apps.defects import services
from apps.common.errors import ConflictError
import uuid

pytestmark = pytest.mark.django_db

def test_add_record_and_list_weekly():
    eid = uuid.uuid4()
    services.add_record({"event_id": eid, "count": Decimal("3.0")})
    items = services.list_amount("weekly")
    assert items[0]["total_defects"] == Decimal("3.0")

    with pytest.raises(ConflictError):
        services.add_record({"event_id": eid, "count": Decimal("1.0")})
