from __future__ import annotations

import uuid

from django.db import migrations, models


def seed_sizes_and_ranks(apps, schema_editor):
    Size = apps.get_model("harvest_api", "Size")
    Rank = apps.get_model("harvest_api", "Rank")

    Size.objects.bulk_create(
        [
            Size(size_id="L", size_name="L"),
            Size(size_id="M", size_name="M"),
            Size(size_id="S", size_name="S"),
            Size(size_id="SS", size_name="SS"),
            Size(size_id="3S", size_name="3S"),
            Size(size_id="小", size_name="極小"),
            Size(size_id="黒", size_name="黒"),
        ],
        ignore_conflicts=True,
    )

    Rank.objects.bulk_create(
        [
            Rank(rank_id="A", rank_name="A品"),
            Rank(rank_id="B", rank_name="B品"),
            Rank(rank_id="C", rank_name="C品"),
            Rank(rank_id="小", rank_name="小"),
            Rank(rank_id="廃棄", rank_name="廃棄"),
        ],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("harvest_api", "0002_harvestrecord_event_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Size",
            fields=[
                ("size_id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("size_name", models.CharField(max_length=255)),
            ],
            options={"db_table": "sizes"},
        ),
        migrations.CreateModel(
            name="Rank",
            fields=[
                ("rank_id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("rank_name", models.CharField(max_length=255)),
            ],
            options={"db_table": "ranks"},
        ),
        migrations.RunPython(seed_sizes_and_ranks, migrations.RunPython.noop),
        migrations.DeleteModel(
            name="HarvestAggregateOverride",
        ),
        migrations.DeleteModel(
            name="HarvestRecord",
        ),
        migrations.CreateModel(
            name="HarvestRecord",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("event_id", models.UUIDField(blank=True, null=True, unique=True)),
                ("lot_name", models.CharField(max_length=64)),
                ("count", models.IntegerField()),
                ("occurred_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("rank", models.ForeignKey(on_delete=models.deletion.PROTECT, to="harvest_api.rank")),
                ("size", models.ForeignKey(on_delete=models.deletion.PROTECT, to="harvest_api.size")),
            ],
            options={"db_table": "harvest_records", "ordering": ["-occurred_at"]},
        ),
        migrations.CreateModel(
            name="HarvestAggregateOverride",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                (
                    "period_type",
                    models.CharField(
                        choices=[("daily", "daily"), ("weekly", "weekly"), ("monthly", "monthly")], max_length=16
                    ),
                ),
                ("period", models.CharField(max_length=16)),
                ("size_name", models.CharField(blank=True, max_length=255, null=True)),
                ("total_count", models.IntegerField()),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("size", models.ForeignKey(on_delete=models.deletion.PROTECT, to="harvest_api.size")),
            ],
            options={
                "db_table": "harvest_aggregate_overrides",
                "unique_together": {("period_type", "period", "size")},
            },
        ),
    ]

