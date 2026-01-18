from decimal import Decimal

from rest_framework import serializers  # type: ignore
from .models import DefectsRecord

class DefectsRecordSerializer(serializers.ModelSerializer):
    count = serializers.DecimalField(max_digits=10, decimal_places=1, coerce_to_string=False)

    class Meta:
        model = DefectsRecord
        fields = ["id", "event_id", "count", "created_at"]

class DefectsAddRequestSerializer(serializers.Serializer):
    """不良品数追加リクエスト（差分アップロード）"""
    event_id = serializers.UUIDField()
    count = serializers.DecimalField(max_digits=10, decimal_places=1, coerce_to_string=False, min_value=Decimal("0.1"))
