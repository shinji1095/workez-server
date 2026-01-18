from __future__ import annotations

import uuid

from django.core.management.base import BaseCommand, CommandError

from apps.prices.models import PriceRecord

DEFAULT_ID_PREFIX = "bada55"


def _normalize_id_prefix(prefix: str) -> str:
    value = prefix.strip().lower().replace("-", "")
    if not value:
        raise CommandError("--id-prefix must not be empty")
    if any(ch not in "0123456789abcdef" for ch in value):
        raise CommandError("--id-prefix must be hex characters")
    if len(value) > 24:
        raise CommandError("--id-prefix must be <= 24 hex chars")
    return value


def _id_range(prefix: str) -> tuple[uuid.UUID, uuid.UUID]:
    remaining = 32 - len(prefix)
    start = uuid.UUID(hex=prefix + ("0" * remaining))
    end = uuid.UUID(hex=prefix + ("f" * remaining))
    return start, end


class Command(BaseCommand):
    help = "Delete dummy price records by id prefix."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--id-prefix",
            default=DEFAULT_ID_PREFIX,
            help="Hex prefix used to mark dummy id values.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only show how many records would be deleted.",
        )

    def handle(self, *args, **options) -> None:
        id_prefix = _normalize_id_prefix(options["id_prefix"])
        dry_run = options["dry_run"]

        start_uuid, end_uuid = _id_range(id_prefix)
        qs = PriceRecord.objects.filter(id__gte=start_uuid, id__lte=end_uuid)
        count = qs.count()

        if dry_run:
            self.stdout.write(
                f"[dry-run] would delete {count} price records with id_prefix={id_prefix}"
            )
            return

        deleted, _ = qs.delete()
        self.stdout.write(
            self.style.SUCCESS(f"Deleted {deleted} price records with id_prefix={id_prefix}")
        )

