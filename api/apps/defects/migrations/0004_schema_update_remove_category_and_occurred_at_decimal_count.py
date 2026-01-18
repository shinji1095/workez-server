from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("defects_api", "0003_remove_device_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="defectsrecord",
            name="occurred_at",
        ),
        migrations.RemoveField(
            model_name="defectsrecord",
            name="category_id",
        ),
        migrations.AlterField(
            model_name="defectsrecord",
            name="count",
            field=models.DecimalField(decimal_places=1, max_digits=10),
        ),
        migrations.AlterModelOptions(
            name="defectsrecord",
            options={"ordering": ["-created_at"]},
        ),
    ]

