import uuid
from django.db import models  # type: ignore

class DefectsRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True, null=True, blank=True)
    count = models.DecimalField(max_digits=10, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "defects_records"
        ordering = ["-created_at"]
