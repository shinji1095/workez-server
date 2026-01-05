import uuid
import pytest
from django.utils import timezone  # type: ignore


pytestmark = pytest.mark.django_db


def test_defects_add_duplicate_event_id_returns_409(device_client):
    eid = str(uuid.uuid4())
    occurred_at = timezone.now().isoformat()

    resp = device_client.post(
        "/defects/amount/add",
        {"event_id": eid, "category_id": "C1", "count": 2, "occurred_at": occurred_at},
        format="json",
    )
    assert resp.status_code == 201

    resp_dup = device_client.post(
        "/defects/amount/add",
        {"event_id": eid, "category_id": "C1", "count": 1, "occurred_at": occurred_at},
        format="json",
    )
    assert resp_dup.status_code == 409
