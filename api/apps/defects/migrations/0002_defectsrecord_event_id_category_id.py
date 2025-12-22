from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("defects_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="defectsrecord",
            name="event_id",
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="defectsrecord",
            name="category_id",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
