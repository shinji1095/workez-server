from rest_framework import serializers  # type: ignore
from .models import HarvestRecord

class HarvestRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestRecord
        fields = ["id", "device_id", "category_id", "category_name", "count", "occurred_at"]

class HarvestAddRequestSerializer(serializers.Serializer):
    """TBD in OpenAPI. Minimal practical payload."""
    device_id = serializers.CharField(max_length=64)
    category_id = serializers.CharField(max_length=32, required=False, allow_null=True)
    category_name = serializers.CharField(max_length=255, required=False, allow_null=True)
    count = serializers.IntegerField(min_value=0)
    occurred_at = serializers.DateTimeField(required=False)

class HarvestOverridePatchRequestSerializer(serializers.Serializer):
    total_count = serializers.IntegerField(min_value=0)

class HarvestTargetUpdateRequestSerializer(serializers.Serializer):
    target_count = serializers.IntegerField(min_value=0)
