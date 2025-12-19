from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DefectsRecord",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("device_id", models.CharField(max_length=64)),
                ("count", models.IntegerField()),
                ("occurred_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table":"defects_records","ordering":["-occurred_at"]},
        ),
    ]
