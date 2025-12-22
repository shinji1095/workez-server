from rest_framework import serializers  # type: ignore
from .models import DefectsRecord

class DefectsRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectsRecord
        fields = ["id", "event_id", "device_id", "category_id", "count", "occurred_at"]

class DefectsAddRequestSerializer(serializers.Serializer):
    """不良品数追加リクエスト（差分アップロード）"""
    event_id = serializers.UUIDField()
    device_id = serializers.CharField(max_length=64)
    category_id = serializers.CharField(max_length=32)
    count = serializers.IntegerField(min_value=1)
    occurred_at = serializers.DateTimeField()
