from __future__ import annotations

from django.db import migrations, models
from django.db.models import F
from django.utils import timezone  # type: ignore


def copy_occurred_at_to_harvested_at(apps, schema_editor):
    HarvestRecord = apps.get_model("harvest_api", "HarvestRecord")
    HarvestRecord.objects.update(harvested_at=F("occurred_at"))


class Migration(migrations.Migration):
    dependencies = [
        ("harvest_api", "0004_harvestrecord_count_decimal"),
    ]

    operations = [
        migrations.RenameField(
            model_name="harvestrecord",
            old_name="created_at",
            new_name="harvested_at",
        ),
        migrations.RunPython(copy_occurred_at_to_harvested_at, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="harvestrecord",
            name="occurred_at",
        ),
        migrations.AlterField(
            model_name="harvestrecord",
            name="harvested_at",
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.AlterModelOptions(
            name="harvestrecord",
            options={"ordering": ["-harvested_at"]},
        ),
    ]

