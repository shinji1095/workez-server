import uuid
from django.db import models  # type: ignore

class DefectsRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True, null=True, blank=True)
    category_id = models.CharField(max_length=64, null=True, blank=True)
    count = models.IntegerField()
    occurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "defects_records"
        ordering = ["-occurred_at"]
