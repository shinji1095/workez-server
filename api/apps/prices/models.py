import uuid
from django.db import models  # type: ignore

class PriceRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.ForeignKey("harvest_api.Size", on_delete=models.PROTECT)
    rank = models.ForeignKey("harvest_api.Rank", on_delete=models.PROTECT)
    unit_price_yen = models.IntegerField()
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "price_records"
        ordering = ["-effective_from"]
        unique_together = ("size", "rank", "effective_from")
