from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("harvest_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="harvestrecord",
            name="event_id",
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
    ]
