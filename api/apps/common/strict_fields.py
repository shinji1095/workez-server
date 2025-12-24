"""Strict serializer fields.

These fields are designed to be *type-strict*.
In particular, they do not coerce string values like "3" into integers.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from rest_framework import serializers  # type: ignore


class StrictUUIDField(serializers.Field):
    """Accept UUID or UUID-string. Reject other types."""

    default_error_messages = {
        "invalid": "Invalid UUID.",
        "type": "Must be a UUID string.",
    }

    def to_internal_value(self, data: Any) -> uuid.UUID:
        if isinstance(data, uuid.UUID):
            return data
        if not isinstance(data, str):
            self.fail("type")
        try:
            return uuid.UUID(data)
        except Exception:
            self.fail("invalid")

    def to_representation(self, value: Any) -> str:
        if isinstance(value, uuid.UUID):
            return str(value)
        return str(uuid.UUID(str(value)))


class StrictPositiveIntField(serializers.Field):
    """Accept int (not bool) and require value >= 1."""

    default_error_messages = {
        "type": "Must be an integer.",
        "min_value": "Must be >= 1.",
    }

    def to_internal_value(self, data: Any) -> int:
        # bool is a subclass of int; reject explicitly.
        if isinstance(data, bool) or not isinstance(data, int):
            self.fail("type")
        if data < 1:
            self.fail("min_value")
        return int(data)

    def to_representation(self, value: Any) -> int:
        return int(value)


class StrictDateTimeField(serializers.Field):
    """Accept ISO8601 string or datetime. Reject other types.

    - If parsed datetime is naive, it will be made aware in the current timezone.
    """

    default_error_messages = {
        "type": "Must be an ISO8601 datetime string.",
        "invalid": "Invalid datetime format.",
    }

    def to_internal_value(self, data: Any) -> datetime:
        if isinstance(data, datetime):
            dt = data
        else:
            if not isinstance(data, str):
                self.fail("type")
            dt = parse_datetime(data)
            if dt is None:
                self.fail("invalid")

        if not is_aware(dt):
            dt = make_aware(dt)
        return dt

    def to_representation(self, value: Any) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        # Fallback
        parsed: Optional[datetime] = parse_datetime(str(value))
        if parsed is None:
            return str(value)
        if not is_aware(parsed):
            parsed = make_aware(parsed)
        return parsed.isoformat()
