from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("defects_api", "0002_defectsrecord_event_id_category_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="defectsrecord",
            name="device_id",
        ),
    ]

