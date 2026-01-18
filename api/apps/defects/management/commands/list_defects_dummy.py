from __future__ import annotations

import uuid

from django.core.management.base import BaseCommand, CommandError

from apps.defects.models import DefectsRecord

DEFAULT_EVENT_ID_PREFIX = "defec7"


def _normalize_event_id_prefix(prefix: str) -> str:
    value = prefix.strip().lower().replace("-", "")
    if not value:
        raise CommandError("--event-id-prefix must not be empty")
    if any(ch not in "0123456789abcdef" for ch in value):
        raise CommandError("--event-id-prefix must be hex characters")
    if len(value) > 24:
        raise CommandError("--event-id-prefix must be <= 24 hex chars")
    return value


def _event_id_range(prefix: str) -> tuple[uuid.UUID, uuid.UUID]:
    remaining = 32 - len(prefix)
    start = uuid.UUID(hex=prefix + ("0" * remaining))
    end = uuid.UUID(hex=prefix + ("f" * remaining))
    return start, end


class Command(BaseCommand):
    help = "List dummy defects records by event_id prefix."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--event-id-prefix",
            default=DEFAULT_EVENT_ID_PREFIX,
            help="Hex prefix used to mark dummy event_id values.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=20,
            help="Number of records to display.",
        )

    def handle(self, *args, **options) -> None:
        event_id_prefix = _normalize_event_id_prefix(options["event_id_prefix"])
        limit = options["limit"]

        if limit <= 0:
            raise CommandError("--limit must be >= 1")

        start_uuid, end_uuid = _event_id_range(event_id_prefix)
        qs = (
            DefectsRecord.objects.filter(event_id__gte=start_uuid, event_id__lte=end_uuid)
            .order_by("-created_at")
        )
        count = qs.count()
        self.stdout.write(f"Found {count} defects records with event_id_prefix={event_id_prefix}")

        for rec in qs[:limit]:
            self.stdout.write(f"{rec.created_at.isoformat()} {rec.event_id} count={rec.count}")

