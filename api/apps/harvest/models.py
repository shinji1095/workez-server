import uuid
from django.db import models  # type: ignore

class Size(models.Model):
    size_id = models.CharField(max_length=64, primary_key=True)
    size_name = models.CharField(max_length=255)

    class Meta:
        db_table = "sizes"


class Rank(models.Model):
    rank_id = models.CharField(max_length=64, primary_key=True)
    rank_name = models.CharField(max_length=255)

    class Meta:
        db_table = "ranks"


class HarvestRecord(models.Model):
    """Harvest record (device events and tablet inputs)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True, null=True, blank=True)
    lot_name = models.CharField(max_length=64)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
    count = models.DecimalField(max_digits=10, decimal_places=1)
    occurred_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "harvest_records"
        ordering = ["-occurred_at"]

class HarvestAggregateOverride(models.Model):
    PERIOD_DAILY = "daily"
    PERIOD_WEEKLY = "weekly"
    PERIOD_MONTHLY = "monthly"
    PERIOD_CHOICES = [
        (PERIOD_DAILY, "daily"),
        (PERIOD_WEEKLY, "weekly"),
        (PERIOD_MONTHLY, "monthly"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    period_type = models.CharField(max_length=16, choices=PERIOD_CHOICES)
    period = models.CharField(max_length=16)  # 'YYYY-MM-DD' / 'YYYY-Www' / 'YYYY-MM'
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    size_name = models.CharField(max_length=255, null=True, blank=True)
    total_count = models.IntegerField()

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "harvest_aggregate_overrides"
        unique_together = ("period_type", "period", "size")

class HarvestTarget(models.Model):
    TARGET_DAILY = "daily"
    TARGET_WEEKLY = "weekly"
    TARGET_MONTHLY = "monthly"
    TARGET_CHOICES = [
        (TARGET_DAILY, "daily"),
        (TARGET_WEEKLY, "weekly"),
        (TARGET_MONTHLY, "monthly"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_type = models.CharField(max_length=16, choices=TARGET_CHOICES, unique=True)
    target_count = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "harvest_targets"
