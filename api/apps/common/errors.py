from __future__ import annotations

from typing import Any

from rest_framework.exceptions import APIException  # type: ignore
from rest_framework import status  # type: ignore


class ConflictError(APIException):
    """409 Conflict.

    Use this only when the API contract explicitly defines conflict cases.
    In this project, it is primarily used for event_id idempotency.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict"
    default_code = "conflict"

    def __init__(self, detail: Any = None):
        super().__init__(detail=detail)
