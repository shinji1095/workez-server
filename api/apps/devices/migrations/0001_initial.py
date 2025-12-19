from django.db import migrations, models
import django.db.models.deletion
import uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                ("id", models.CharField(primary_key=True, max_length=64, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("status", models.CharField(choices=[("active","active"),("inactive","inactive"),("maintenance","maintenance")], default="active", max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table":"devices","ordering":["id"]},
        ),
        migrations.CreateModel(
            name="BatteryStatus",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, auto_created=True, verbose_name="ID")),
                ("percent", models.IntegerField()),
                ("voltage_mv", models.IntegerField(null=True, blank=True)),
                ("is_charging", models.BooleanField(default=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("device", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="battery_status", to="devices_api.device")),
            ],
            options={"db_table":"device_battery_status"},
        ),
        migrations.CreateModel(
            name="Alarm",
            fields=[
                ("alarm_id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("type", models.CharField(choices=[("battery_low","battery_low"),("sensor_failure","sensor_failure"),("network_error","network_error")], max_length=32)),
                ("message", models.TextField()),
                ("status", models.CharField(choices=[("open","open"),("acknowledged","acknowledged"),("closed","closed")], default="open", max_length=32)),
                ("severity", models.CharField(choices=[("info","info"),("warning","warning"),("critical","critical")], null=True, blank=True, max_length=16)),
                ("occurred_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="alarms", to="devices_api.device")),
            ],
            options={"db_table":"device_alarms","ordering":["-occurred_at"]},
        ),
    ]
