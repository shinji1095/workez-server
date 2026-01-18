from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="user",
            table="users",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_active",
        ),
    ]

