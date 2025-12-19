import uuid
from django.db import models  # type: ignore

class HarvestRecord(models.Model):
    """Raw harvest events uploaded from devices."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=64)
    category_id = models.CharField(max_length=32, null=True, blank=True)
    category_name = models.CharField(max_length=255, null=True, blank=True)
    count = models.IntegerField()
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
    category_id = models.CharField(max_length=32)
    category_name = models.CharField(max_length=255, null=True, blank=True)
    total_count = models.IntegerField()

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "harvest_aggregate_overrides"
        unique_together = ("period_type", "period", "category_id")

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
