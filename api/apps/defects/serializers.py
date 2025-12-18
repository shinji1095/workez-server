from rest_framework import serializers  # type: ignore
from .models import DefectsRecord

class DefectsRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectsRecord
        fields = ["id", "device_id", "count", "occurred_at"]

class DefectsAddRequestSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=64)
    count = serializers.IntegerField(min_value=0)
    occurred_at = serializers.DateTimeField(required=False)
