from rest_framework import serializers  # type: ignore
from .models import HarvestRecord

class HarvestRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestRecord
        fields = ["id", "event_id", "device_id", "category_id", "category_name", "count", "occurred_at"]

class HarvestAddRequestSerializer(serializers.Serializer):
    """収穫数追加リクエスト（差分アップロード）"""
    event_id = serializers.UUIDField()
    device_id = serializers.CharField(max_length=64)
    category_id = serializers.CharField(max_length=32)
    count = serializers.IntegerField(min_value=1)
    occurred_at = serializers.DateTimeField()

class HarvestOverridePatchRequestSerializer(serializers.Serializer):
    total_count = serializers.IntegerField(min_value=0)

class HarvestTargetUpdateRequestSerializer(serializers.Serializer):
    target_count = serializers.IntegerField(min_value=0)
