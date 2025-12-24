# tests/test_harvest.py
import uuid
import pytest
from django.utils import timezone  # type: ignore

try:
    # DRF is assumed in this project (APIClient fixtures exist)
    from rest_framework.test import APIClient  # type: ignore
except Exception:  # pragma: no cover
    APIClient = None  # type: ignore


pytestmark = pytest.mark.django_db


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def _anon_client():
    """Unauthenticated client (no JWT)."""
    if APIClient is None:  # pragma: no cover
        raise RuntimeError("rest_framework is not available. Install DRF or provide anon_client fixture.")
    return APIClient()


def _payload(resp):
    """
    DRF's APIClient may return a response with `.data`,
    while Django test client response provides `.json()`.
    """
    if hasattr(resp, "data"):
        return resp.data
    return resp.json()


def _assert_success_envelope(resp):
    body = _payload(resp)
    assert isinstance(body, dict)
    # openapi.yaml requires `status` and `data`, but test_cases.md mentions only `data`.
    # Keep strict on `data`, and soft-check `status` type if present.
    assert "data" in body
    if "status" in body:
        assert isinstance(body["status"], str)
    return body["data"]


def _assert_error_envelope(resp):
    body = _payload(resp)
    assert isinstance(body, dict)
    assert "error" in body
    err = body["error"]
    assert isinstance(err, dict)
    # openapi.yaml requires these keys
    for k in ("code", "message", "details", "request_id"):
        assert k in err
    assert isinstance(err["details"], list)


def _prepare_price(admin_client, category_id: str, unit_price_yen: int = 100, effective_from: str = "2025-01-01"):
    """
    For harvest aggregation, price/category existence is often required.
    Your current test already uses this endpoint as prerequisite.
    """
    resp = admin_client.post(
        f"/prices/category/{category_id}",
        {"unit_price_yen": unit_price_yen, "effective_from": effective_from},
        format="json",
    )
    # Spec: 201. If implementation returns 200 for upsert, allow it.
    assert resp.status_code in (200, 201), _payload(resp)
    _assert_success_envelope(resp)


def _add_harvest(
    device_client,
    *,
    event_id: str,
    device_id: str,
    category_id: str,
    count: int,
    occurred_at: str,
):
    return device_client.post(
        "/harvest/amount/add",
        {
            "event_id": event_id,
            "device_id": device_id,
            "category_id": category_id,
            "count": count,
            "occurred_at": occurred_at,
        },
        format="json",
    )


# -----------------------------------------------------------------------------
# POST /harvest/amount/add (device only)
# -----------------------------------------------------------------------------
def test_create_harvest_amount_add_success(device_client, admin_client):
    category_id = "C1"
    device_id = "D1"
    occurred_at = "2025-01-15T09:00:00+09:00"

    _prepare_price(admin_client, category_id)

    resp = _add_harvest(
        device_client,
        event_id=str(uuid.uuid4()),
        device_id=device_id,
        category_id=category_id,
        count=3,
        occurred_at=occurred_at,
    )
    assert resp.status_code == 201, _payload(resp)

    data = _assert_success_envelope(resp)
    # HarvestRecord required fields in openapi.yaml
    for k in ("id", "device_id", "count", "occurred_at", "created_at"):
        assert k in data
    assert data["device_id"] == device_id
    assert data["count"] == 3


def test_create_harvest_amount_add_duplicate_event_id_conflict(device_client, admin_client):
    category_id = "C1"
    device_id = "D1"
    occurred_at = "2025-01-15T09:00:00+09:00"

    _prepare_price(admin_client, category_id)

    event_id = str(uuid.uuid4())
    resp1 = _add_harvest(
        device_client,
        event_id=event_id,
        device_id=device_id,
        category_id=category_id,
        count=3,
        occurred_at=occurred_at,
    )
    assert resp1.status_code == 201, _payload(resp1)

    resp2 = _add_harvest(
        device_client,
        event_id=event_id,
        device_id=device_id,
        category_id=category_id,
        count=1,
        occurred_at=occurred_at,
    )
    assert resp2.status_code == 409, _payload(resp2)
    _assert_error_envelope(resp2)


def test_create_harvest_amount_add_requires_auth_and_device_role(user_client, admin_client, device_client):
    category_id = "C1"
    device_id = "D1"
    occurred_at = "2025-01-15T09:00:00+09:00"

    _prepare_price(admin_client, category_id)

    payload = {
        "event_id": str(uuid.uuid4()),
        "device_id": device_id,
        "category_id": category_id,
        "count": 3,
        "occurred_at": occurred_at,
    }

    anon = _anon_client()
    r0 = anon.post("/harvest/amount/add", payload, format="json")
    assert r0.status_code == 401, _payload(r0)
    _assert_error_envelope(r0)

    r1 = user_client.post("/harvest/amount/add", payload, format="json")
    assert r1.status_code == 403, _payload(r1)
    _assert_error_envelope(r1)

    r2 = admin_client.post("/harvest/amount/add", payload, format="json")
    assert r2.status_code == 403, _payload(r2)
    _assert_error_envelope(r2)

    r3 = device_client.post("/harvest/amount/add", payload, format="json")
    assert r3.status_code in (201, 409, 400), _payload(r3)
    # device role itself is accepted; outcome depends on payload validity / duplication.


@pytest.mark.parametrize(
    "mutate, expected_status",
    [
        (lambda p: p.pop("event_id"), 400),
        (lambda p: p.__setitem__("event_id", "not-a-uuid"), 400),
        (lambda p: p.pop("device_id"), 400),
        (lambda p: p.pop("category_id"), 400),
        (lambda p: p.pop("count"), 400),
        (lambda p: p.__setitem__("count", 0), 400),   # boundary: minimum is 1
        (lambda p: p.__setitem__("count", -1), 400),
        (lambda p: p.__setitem__("count", "3"), 400),
        (lambda p: p.pop("occurred_at"), 400),
        (lambda p: p.__setitem__("occurred_at", "2025-99-99"), 400),
        (lambda p: p.__setitem__("occurred_at", "not-a-datetime"), 400),
    ],
)
def test_create_harvest_amount_add_invalid_input_returns_400(device_client, admin_client, mutate, expected_status):
    category_id = "C1"
    device_id = "D1"
    occurred_at = "2025-01-15T09:00:00+09:00"

    _prepare_price(admin_client, category_id)

    payload = {
        "event_id": str(uuid.uuid4()),
        "device_id": device_id,
        "category_id": category_id,
        "count": 3,
        "occurred_at": occurred_at,
    }
    mutate(payload)

    resp = device_client.post("/harvest/amount/add", payload, format="json")
    assert resp.status_code == expected_status, _payload(resp)
    _assert_error_envelope(resp)


def test_create_harvest_amount_add_count_boundary_values(device_client, admin_client):
    category_id = "C1"
    device_id = "D1"
    occurred_at = "2025-01-15T09:00:00+09:00"
    _prepare_price(admin_client, category_id)

    # minimum=1 should pass
    resp_ok = _add_harvest(
        device_client,
        event_id=str(uuid.uuid4()),
        device_id=device_id,
        category_id=category_id,
        count=1,
        occurred_at=occurred_at,
    )
    assert resp_ok.status_code == 201, _payload(resp_ok)
    data = _assert_success_envelope(resp_ok)
    assert data["count"] == 1

    # 0 should fail
    resp_ng = _add_harvest(
        device_client,
        event_id=str(uuid.uuid4()),
        device_id=device_id,
        category_id=category_id,
        count=0,
        occurred_at=occurred_at,
    )
    assert resp_ng.status_code == 400, _payload(resp_ng)
    _assert_error_envelope(resp_ng)


# -----------------------------------------------------------------------------
# GET /harvest/amount/daily (user/admin; device forbidden)
# -----------------------------------------------------------------------------
def test_list_harvest_amount_daily_success_contains_aggregate(device_client, user_client, admin_client):
    category_id = "C1"
    device_id = "D1"
    occurred_at = "2025-01-15T09:00:00+09:00"
    target_period = "2025-01-15"

    _prepare_price(admin_client, category_id)

    resp_add = _add_harvest(
        device_client,
        event_id=str(uuid.uuid4()),
        device_id=device_id,
        category_id=category_id,
        count=3,
        occurred_at=occurred_at,
    )
    assert resp_add.status_code == 201, _payload(resp_add)

    resp = user_client.get("/harvest/amount/daily?page=1&page_size=50")
    assert resp.status_code == 200, _payload(resp)

    data = _assert_success_envelope(resp)
    # Paginated response shape (items/page/page_size/total)
    for k in ("items", "page", "page_size", "total"):
        assert k in data
    assert isinstance(data["items"], list)

    # At least one aggregated row should reflect what we added (period + category + total_count)
    found = False
    for item in data["items"]:
        if (
            item.get("period") == target_period
            and item.get("category_id") == category_id
            and item.get("total_count") == 3
        ):
            found = True
            break
    assert found, data["items"]


def test_list_harvest_amount_daily_requires_auth_and_permission(device_client, user_client, admin_client):
    anon = _anon_client()

    r0 = anon.get("/harvest/amount/daily?page=1&page_size=10")
    assert r0.status_code == 401, _payload(r0)
    _assert_error_envelope(r0)

    r1 = device_client.get("/harvest/amount/daily?page=1&page_size=10")
    assert r1.status_code == 403, _payload(r1)
    _assert_error_envelope(r1)

    r2 = user_client.get("/harvest/amount/daily?page=1&page_size=10")
    assert r2.status_code == 200, _payload(r2)

    r3 = admin_client.get("/harvest/amount/daily?page=1&page_size=10")
    assert r3.status_code == 200, _payload(r3)


@pytest.mark.parametrize(
    "qs",
    [
        "page=0&page_size=10",
        "page=-1&page_size=10",
        "page=1&page_size=0",
        "page=1&page_size=501",
        "page=1&page_size=-1",
    ],
)
def test_list_harvest_amount_daily_pagination_boundaries(user_client, qs):
    resp = user_client.get(f"/harvest/amount/daily?{qs}")
    assert resp.status_code == 400, _payload(resp)
    _assert_error_envelope(resp)


# -----------------------------------------------------------------------------
# GET /harvest/amount/daily/category/{categoryId} (user/admin; device forbidden)
# -----------------------------------------------------------------------------
def test_retrieve_harvest_amount_daily_category_success(device_client, user_client, admin_client):
    category_id = "C1"
    device_id = "D1"
    occurred_at = "2025-01-15T09:00:00+09:00"
    target_period = "2025-01-15"

    _prepare_price(admin_client, category_id)

    resp_add = _add_harvest(
        device_client,
        event_id=str(uuid.uuid4()),
        device_id=device_id,
        category_id=category_id,
        count=3,
        occurred_at=occurred_at,
    )
    assert resp_add.status_code == 201, _payload(resp_add)

    resp = user_client.get(f"/harvest/amount/daily/category/{category_id}?page=1&page_size=50")
    assert resp.status_code == 200, _payload(resp)

    data = _assert_success_envelope(resp)
    for k in ("items", "page", "page_size", "total"):
        assert k in data

    # Items may still include category_id in this spec; at minimum ensure the period appears.
    assert any(item.get("period") == target_period for item in data["items"]), data["items"]


def test_retrieve_harvest_amount_daily_category_not_found(user_client):
    resp = user_client.get("/harvest/amount/daily/category/NO_SUCH_CATEGORY?page=1&page_size=10")
    assert resp.status_code == 404, _payload(resp)
    _assert_error_envelope(resp)


def test_retrieve_harvest_amount_daily_category_requires_auth_and_permission(device_client, user_client):
    anon = _anon_client()

    r0 = anon.get("/harvest/amount/daily/category/C1?page=1&page_size=10")
    assert r0.status_code == 401, _payload(r0)
    _assert_error_envelope(r0)

    r1 = device_client.get("/harvest/amount/daily/category/C1?page=1&page_size=10")
    assert r1.status_code == 403, _payload(r1)
    _assert_error_envelope(r1)

    r2 = user_client.get("/harvest/amount/daily/category/C1?page=1&page_size=10")
    assert r2.status_code in (200, 404), _payload(r2)
    # 404 is possible if category does not exist in this test context.


@pytest.mark.parametrize(
    "qs",
    [
        "page=0&page_size=10",
        "page=1&page_size=0",
        "page=1&page_size=501",
    ],
)
def test_retrieve_harvest_amount_daily_category_pagination_boundaries(user_client, qs):
    resp = user_client.get(f"/harvest/amount/daily/category/C1?{qs}")
    assert resp.status_code == 400, _payload(resp)
    _assert_error_envelope(resp)


# -----------------------------------------------------------------------------
# Optional: smoke tests for weekly/monthly list endpoints (auth + pagination only)
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "path",
    [
        "/harvest/amount/weekly",
        "/harvest/amount/monthly",
    ],
)
def test_list_harvest_amount_weekly_monthly_auth_and_pagination_smoke(device_client, user_client, path):
    anon = _anon_client()

    r0 = anon.get(f"{path}?page=1&page_size=10")
    assert r0.status_code == 401, _payload(r0)
    _assert_error_envelope(r0)

    r1 = device_client.get(f"{path}?page=1&page_size=10")
    assert r1.status_code == 403, _payload(r1)
    _assert_error_envelope(r1)

    r2 = user_client.get(f"{path}?page=1&page_size=10")
    assert r2.status_code == 200, _payload(r2)
    _assert_success_envelope(r2)

    r3 = user_client.get(f"{path}?page=0&page_size=10")
    assert r3.status_code == 400, _payload(r3)
    _assert_error_envelope(r3)

    r4 = user_client.get(f"{path}?page=1&page_size=501")
    assert r4.status_code == 400, _payload(r4)
    _assert_error_envelope(r4)
