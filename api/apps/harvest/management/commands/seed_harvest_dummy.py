from __future__ import annotations

import random
import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Dict, List, Sequence

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.harvest.models import HarvestRecord, Rank, Size

DEFAULT_EVENT_ID_PREFIX = "d00d5eed"
DEFAULT_LOT_NAMES = ("1a", "1b", "2e")
DEFAULT_SIZE_IDS = ("L", "M", "S")
DEFAULT_RANK_IDS = ("A", "B")
DEFAULT_MIN_COUNT = Decimal("0.1")
DEFAULT_MAX_COUNT = Decimal("5")
COUNT_STEP = Decimal("0.1")


def _parse_csv(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _ensure_sizes(size_ids: Sequence[str]) -> Dict[str, Size]:
    sizes: Dict[str, Size] = {}
    for size_id in size_ids:
        size, _ = Size.objects.get_or_create(
            size_id=size_id,
            defaults={"size_name": size_id},
        )
        sizes[size_id] = size
    return sizes


def _ensure_ranks(rank_ids: Sequence[str]) -> Dict[str, Rank]:
    ranks: Dict[str, Rank] = {}
    for rank_id in rank_ids:
        rank, _ = Rank.objects.get_or_create(
            rank_id=rank_id,
            defaults={"rank_name": rank_id},
        )
        ranks[rank_id] = rank
    return ranks


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
    help = "Insert dummy harvest records."

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
            "--lot-names",
            default=",".join(DEFAULT_LOT_NAMES),
            help="Comma-separated lot names to use.",
        )
        parser.add_argument(
            "--size-ids",
            default=",".join(DEFAULT_SIZE_IDS),
            help="Comma-separated size IDs to use.",
        )
        parser.add_argument(
            "--rank-ids",
            default=",".join(DEFAULT_RANK_IDS),
            help="Comma-separated rank IDs to use.",
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
        lot_names = _parse_csv(options["lot_names"])
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
        if not lot_names:
            raise CommandError("--lot-names must not be empty")
        if max_count < min_count:
            raise CommandError("--max-count must be >= --min-count")
        min_units = int((min_count / COUNT_STEP).to_integral_value())
        max_units = int((max_count / COUNT_STEP).to_integral_value())
        if batch_size <= 0:
            raise CommandError("--batch-size must be >= 1")

        size_ids = _parse_csv(options["size_ids"])
        rank_ids = _parse_csv(options["rank_ids"])
        if not size_ids:
            raise CommandError("--size-ids must not be empty")
        if not rank_ids:
            raise CommandError("--rank-ids must not be empty")

        start_date_str = options["start_date"]
        if start_date_str:
            try:
                start_date = date.fromisoformat(start_date_str)
            except ValueError as exc:
                raise CommandError("--start-date must be YYYY-MM-DD") from exc
        else:
            start_date = timezone.localdate()

        sizes = _ensure_sizes(size_ids)
        ranks = _ensure_ranks(rank_ids)

        rng = random.Random(seed)
        tz = timezone.get_current_timezone()

        records: List[HarvestRecord] = []
        event_ids: List[uuid.UUID] = []
        seen_event_ids: set[uuid.UUID] = set()

        for day_offset in range(days):
            day = start_date - timedelta(days=day_offset)
            for idx in range(per_day):
                size_id = rng.choice(size_ids)
                rank_id = rng.choice(rank_ids)
                lot_name = rng.choice(lot_names)
                count_units = rng.randint(min_units, max_units)
                count = (Decimal(count_units) * COUNT_STEP).quantize(COUNT_STEP)
                hour = rng.randint(6, 18)
                minute = rng.randint(0, 59)
                second = rng.randint(0, 59)
                occurred_at = datetime.combine(day, time(hour=hour, minute=minute, second=second))
                occurred_at = timezone.make_aware(occurred_at, tz)
                event_id = _random_uuid_with_prefix(rng, event_id_prefix)
                while event_id in seen_event_ids:
                    event_id = _random_uuid_with_prefix(rng, event_id_prefix)
                seen_event_ids.add(event_id)

                event_ids.append(event_id)
                records.append(
                    HarvestRecord(
                        event_id=event_id,
                        lot_name=lot_name,
                        size=sizes[size_id],
                        rank=ranks[rank_id],
                        count=count,
                        occurred_at=occurred_at,
                    )
                )

        existing = set(
            HarvestRecord.objects.filter(event_id__in=event_ids).values_list("event_id", flat=True)
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
            HarvestRecord.objects.bulk_create(records, batch_size=batch_size)

        self.stdout.write(self.style.SUCCESS(f"Inserted {to_create} harvest records."))
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
