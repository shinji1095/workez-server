from __future__ import annotations

import random
import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import List

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.defects.models import DefectsRecord

DEFAULT_EVENT_ID_PREFIX = "defec7"
DEFAULT_MIN_COUNT = Decimal("0.1")
DEFAULT_MAX_COUNT = Decimal("3.0")
COUNT_STEP = Decimal("0.1")


def _normalize_event_id_prefix(prefix: str) -> str:
    value = prefix.strip().lower().replace("-", "")
    if not value:
        raise CommandError("--event-id-prefix must not be empty")
    if any(ch not in "0123456789abcdef" for ch in value):
        raise CommandError("--event-id-prefix must be hex characters")
    if len(value) > 24:
        raise CommandError("--event-id-prefix must be <= 24 hex chars")
    return value


def _random_uuid_with_prefix(rng: random.Random, prefix: str) -> uuid.UUID:
    remaining = 32 - len(prefix)
    suffix = "".join(rng.choice("0123456789abcdef") for _ in range(remaining))
    return uuid.UUID(hex=prefix + suffix)


def _parse_count(value: str, name: str) -> Decimal:
    try:
        dec = Decimal(value)
    except Exception as exc:
        raise CommandError(f"{name} must be a decimal") from exc
    if dec < COUNT_STEP:
        raise CommandError(f"{name} must be >= {COUNT_STEP}")
    if dec != dec.quantize(COUNT_STEP):
        raise CommandError(f"{name} must be in {COUNT_STEP} increments")
    return dec


class Command(BaseCommand):
    help = "Insert dummy defects records."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Number of days to generate (inclusive, counting back from start-date).",
        )
        parser.add_argument(
            "--per-day",
            type=int,
            default=20,
            help="Number of records per day.",
        )
        parser.add_argument(
            "--start-date",
            default="",
            help="Start date in YYYY-MM-DD. Defaults to today (local time).",
        )
        parser.add_argument(
            "--event-id-prefix",
            default=DEFAULT_EVENT_ID_PREFIX,
            help="Hex prefix used to mark dummy event_id values.",
        )
        parser.add_argument(
            "--min-count",
            default=str(DEFAULT_MIN_COUNT),
            help="Minimum count per record (decimal, 0.1 step).",
        )
        parser.add_argument(
            "--max-count",
            default=str(DEFAULT_MAX_COUNT),
            help="Maximum count per record (decimal, 0.1 step).",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=0,
            help="Random seed for reproducible dummy data.",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=500,
            help="bulk_create batch size.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only show how many records would be created.",
        )

    def handle(self, *args, **options) -> None:
        days = options["days"]
        per_day = options["per_day"]
        min_count = _parse_count(options["min_count"], "--min-count")
        max_count = _parse_count(options["max_count"], "--max-count")
        seed = options["seed"]
        batch_size = options["batch_size"]
        dry_run = options["dry_run"]
        event_id_prefix = _normalize_event_id_prefix(options["event_id_prefix"])

        if days <= 0:
            raise CommandError("--days must be >= 1")
        if per_day <= 0:
            raise CommandError("--per-day must be >= 1")
        if max_count < min_count:
            raise CommandError("--max-count must be >= --min-count")
        min_units = int((min_count / COUNT_STEP).to_integral_value())
        max_units = int((max_count / COUNT_STEP).to_integral_value())
        if batch_size <= 0:
            raise CommandError("--batch-size must be >= 1")

        start_date_str = options["start_date"]
        if start_date_str:
            try:
                start_date = date.fromisoformat(start_date_str)
            except ValueError as exc:
                raise CommandError("--start-date must be YYYY-MM-DD") from exc
        else:
            start_date = timezone.localdate()

        rng = random.Random(seed)
        tz = timezone.get_current_timezone()

        records: List[DefectsRecord] = []
        event_ids: List[uuid.UUID] = []
        seen_event_ids: set[uuid.UUID] = set()

        for day_offset in range(days):
            day = start_date - timedelta(days=day_offset)
            for _ in range(per_day):
                count_units = rng.randint(min_units, max_units)
                count = (Decimal(count_units) * COUNT_STEP).quantize(COUNT_STEP)
                hour = rng.randint(6, 20)
                minute = rng.randint(0, 59)
                second = rng.randint(0, 59)
                created_at = datetime.combine(day, time(hour=hour, minute=minute, second=second))
                created_at = timezone.make_aware(created_at, tz)
                event_id = _random_uuid_with_prefix(rng, event_id_prefix)
                while event_id in seen_event_ids:
                    event_id = _random_uuid_with_prefix(rng, event_id_prefix)
                seen_event_ids.add(event_id)

                event_ids.append(event_id)
                records.append(
                    DefectsRecord(
                        event_id=event_id,
                        count=count,
                        created_at=created_at,
                    )
                )

        existing = set(
            DefectsRecord.objects.filter(event_id__in=event_ids).values_list("event_id", flat=True)
        )
        if existing:
            records = [record for record in records if record.event_id not in existing]

        total = len(event_ids)
        skipped = len(existing)
        to_create = len(records)

        if dry_run:
            self.stdout.write(
                f"[dry-run] would create {to_create} records "
                f"(skipping {skipped} existing) out of {total} generated."
            )
            return

        if to_create:
            DefectsRecord.objects.bulk_create(records, batch_size=batch_size)

        self.stdout.write(self.style.SUCCESS(f"Inserted {to_create} defects records."))
        if skipped:
            self.stdout.write(self.style.WARNING(f"Skipped {skipped} existing records."))
        self.stdout.write(
            "event_id_prefix={} start_date={} days={} per_day={} seed={}".format(
                event_id_prefix,
                start_date.isoformat(),
                days,
                per_day,
                seed,
            )
        )

