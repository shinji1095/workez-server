from __future__ import annotations

import random
import uuid
from datetime import date
from typing import Dict, List, Sequence, Tuple

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.harvest.models import Rank, Size
from apps.prices.models import PriceRecord

DEFAULT_ID_PREFIX = "bada55"
DEFAULT_SIZE_IDS = ("L", "M", "S")
DEFAULT_RANK_IDS = ("A", "B")
DEFAULT_MIN_PRICE = 100
DEFAULT_MAX_PRICE = 600


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


def _normalize_id_prefix(prefix: str) -> str:
    value = prefix.strip().lower().replace("-", "")
    if not value:
        raise CommandError("--id-prefix must not be empty")
    if any(ch not in "0123456789abcdef" for ch in value):
        raise CommandError("--id-prefix must be hex characters")
    if len(value) > 24:
        raise CommandError("--id-prefix must be <= 24 hex chars")
    return value


def _random_uuid_with_prefix(rng: random.Random, prefix: str) -> uuid.UUID:
    remaining = 32 - len(prefix)
    suffix = "".join(rng.choice("0123456789abcdef") for _ in range(remaining))
    return uuid.UUID(hex=prefix + suffix)


class Command(BaseCommand):
    help = "Insert dummy price records."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--months",
            type=int,
            default=12,
            help="Number of months to generate (inclusive, counting back from start-date).",
        )
        parser.add_argument(
            "--per-month",
            type=int,
            default=6,
            help="Number of records per month.",
        )
        parser.add_argument(
            "--start-date",
            default="",
            help="Start date in YYYY-MM-DD. Defaults to today (local time).",
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
            "--min-price",
            type=int,
            default=DEFAULT_MIN_PRICE,
            help="Minimum unit price (yen).",
        )
        parser.add_argument(
            "--max-price",
            type=int,
            default=DEFAULT_MAX_PRICE,
            help="Maximum unit price (yen).",
        )
        parser.add_argument(
            "--id-prefix",
            default=DEFAULT_ID_PREFIX,
            help="Hex prefix used to mark dummy id values.",
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
        months = options["months"]
        per_month = options["per_month"]
        min_price = options["min_price"]
        max_price = options["max_price"]
        seed = options["seed"]
        batch_size = options["batch_size"]
        dry_run = options["dry_run"]
        id_prefix = _normalize_id_prefix(options["id_prefix"])

        if months <= 0:
            raise CommandError("--months must be >= 1")
        if per_month <= 0:
            raise CommandError("--per-month must be >= 1")
        if min_price < 0:
            raise CommandError("--min-price must be >= 0")
        if max_price < min_price:
            raise CommandError("--max-price must be >= --min-price")
        if batch_size <= 0:
            raise CommandError("--batch-size must be >= 1")

        size_ids = _parse_csv(options["size_ids"])
        rank_ids = _parse_csv(options["rank_ids"])
        if not size_ids:
            raise CommandError("--size-ids must not be empty")
        if not rank_ids:
            raise CommandError("--rank-ids must not be empty")

        combos: List[Tuple[str, str]] = [(s, r) for s in size_ids for r in rank_ids]
        if per_month > len(combos):
            raise CommandError("--per-month must be <= size_ids * rank_ids")

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
        now = timezone.now()

        records: List[PriceRecord] = []
        seen_ids: set[uuid.UUID] = set()
        seen_pairs: set[Tuple[str, str, int, int]] = set(
            PriceRecord.objects.values_list("size__size_id", "rank__rank_id", "year", "month")
        )

        start_month = date(start_date.year, start_date.month, 1)
        for month_offset in range(months):
            year = start_month.year
            month = start_month.month - month_offset
            while month <= 0:
                year -= 1
                month += 12
            monthly_combos = combos[:]
            rng.shuffle(monthly_combos)
            for size_id, rank_id in monthly_combos[:per_month]:
                key = (size_id, rank_id, year, month)
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                unit_price = rng.randint(min_price, max_price)
                record_id = _random_uuid_with_prefix(rng, id_prefix)
                while record_id in seen_ids:
                    record_id = _random_uuid_with_prefix(rng, id_prefix)
                seen_ids.add(record_id)
                records.append(
                    PriceRecord(
                        id=record_id,
                        size=sizes[size_id],
                        rank=ranks[rank_id],
                        unit_price_yen=unit_price,
                        year=year,
                        month=month,
                        updated_at=now,
                    )
                )

        total = len(records)

        if dry_run:
            self.stdout.write(f"[dry-run] would create {total} price records.")
            return

        if total:
            PriceRecord.objects.bulk_create(records, batch_size=batch_size)

        self.stdout.write(self.style.SUCCESS(f"Inserted {total} price records."))
        self.stdout.write(
            "id_prefix={} start_date={} months={} per_month={} seed={}".format(
                id_prefix,
                start_date.isoformat(),
                months,
                per_month,
                seed,
            )
        )

