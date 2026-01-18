from __future__ import annotations

import calendar
from datetime import date

from django.db import migrations, models


def forwards_fill_year_month(apps, schema_editor) -> None:
    PriceRecord = apps.get_model("prices_api", "PriceRecord")
    for rec in PriceRecord.objects.all().only("id", "effective_from").iterator():
        if rec.effective_from:
            rec.year = rec.effective_from.year
            rec.month = rec.effective_from.month
            rec.save(update_fields=["year", "month"])


def backwards_fill_effective_dates(apps, schema_editor) -> None:
    PriceRecord = apps.get_model("prices_api", "PriceRecord")
    for rec in PriceRecord.objects.all().only("id", "year", "month").iterator():
        if rec.year and rec.month:
            rec.effective_from = date(rec.year, rec.month, 1)
            last_day = calendar.monthrange(rec.year, rec.month)[1]
            rec.effective_to = date(rec.year, rec.month, last_day)
            rec.save(update_fields=["effective_from", "effective_to"])


class Migration(migrations.Migration):
    dependencies = [
        ("prices_api", "0002_size_rank_schema_update"),
    ]

    operations = [
        migrations.AddField(
            model_name="pricerecord",
            name="year",
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="pricerecord",
            name="month",
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.RunPython(forwards_fill_year_month, backwards_fill_effective_dates),
        migrations.AlterField(
            model_name="pricerecord",
            name="year",
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name="pricerecord",
            name="month",
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name="pricerecord",
            unique_together={("size", "rank", "year", "month")},
        ),
        migrations.RemoveField(
            model_name="pricerecord",
            name="effective_from",
        ),
        migrations.RemoveField(
            model_name="pricerecord",
            name="effective_to",
        ),
        migrations.AlterModelOptions(
            name="pricerecord",
            options={"ordering": ["-year", "-month"]},
        ),
    ]

