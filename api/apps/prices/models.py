import uuid
from django.db import models  # type: ignore

class PriceRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_id = models.CharField(max_length=32)
    category_name = models.CharField(max_length=255, null=True, blank=True)
    unit_price_yen = models.IntegerField()
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "price_records"
        ordering = ["-effective_from"]
        unique_together = ("category_id", "effective_from")
