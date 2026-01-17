from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("harvest_api", "0003_sizes_ranks_and_schema_update"),
    ]

    operations = [
        migrations.AlterField(
            model_name="harvestrecord",
            name="count",
            field=models.DecimalField(decimal_places=1, max_digits=10),
        ),
    ]
