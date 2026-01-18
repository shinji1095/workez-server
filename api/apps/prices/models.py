import uuid
from django.db import models  # type: ignore

class PriceRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.ForeignKey("harvest_api.Size", on_delete=models.PROTECT)
    rank = models.ForeignKey("harvest_api.Rank", on_delete=models.PROTECT)
    unit_price_yen = models.IntegerField()
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "price_records"
        ordering = ["-year", "-month"]
        unique_together = ("size", "rank", "year", "month")
