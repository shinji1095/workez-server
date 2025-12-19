from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HarvestRecord",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("device_id", models.CharField(max_length=64)),
                ("category_id", models.CharField(max_length=32, null=True, blank=True)),
                ("category_name", models.CharField(max_length=255, null=True, blank=True)),
                ("count", models.IntegerField()),
                ("occurred_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table":"harvest_records","ordering":["-occurred_at"]},
        ),
        migrations.CreateModel(
            name="HarvestAggregateOverride",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("period_type", models.CharField(choices=[("daily","daily"),("weekly","weekly"),("monthly","monthly")], max_length=16)),
                ("period", models.CharField(max_length=16)),
                ("category_id", models.CharField(max_length=32)),
                ("category_name", models.CharField(max_length=255, null=True, blank=True)),
                ("total_count", models.IntegerField()),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table":"harvest_aggregate_overrides","unique_together":{("period_type","period","category_id")}},
        ),
        migrations.CreateModel(
            name="HarvestTarget",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("target_type", models.CharField(choices=[("daily","daily"),("weekly","weekly"),("monthly","monthly")], max_length=16, unique=True)),
                ("target_count", models.IntegerField()),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table":"harvest_targets"},
        ),
    ]
