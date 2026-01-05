from __future__ import annotations

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("harvest_api", "0003_sizes_ranks_and_schema_update"),
        ("prices_api", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PriceRecord",
        ),
        migrations.CreateModel(
            name="PriceRecord",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("unit_price_yen", models.IntegerField()),
                ("effective_from", models.DateField()),
                ("effective_to", models.DateField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("rank", models.ForeignKey(on_delete=models.deletion.PROTECT, to="harvest_api.rank")),
                ("size", models.ForeignKey(on_delete=models.deletion.PROTECT, to="harvest_api.size")),
            ],
            options={
                "db_table": "price_records",
                "ordering": ["-effective_from"],
                "unique_together": {("size", "rank", "effective_from")},
            },
        ),
    ]

