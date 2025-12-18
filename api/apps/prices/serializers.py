from rest_framework import serializers  # type: ignore
from .models import PriceRecord

class PriceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRecord
        fields = ["category_id", "category_name", "unit_price_yen", "effective_from", "effective_to", "updated_at"]

class CreatePriceCategoryRequestSerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=255, required=False, allow_null=True)
    unit_price_yen = serializers.IntegerField(min_value=0)
    effective_from = serializers.DateField()
    effective_to = serializers.DateField(required=False, allow_null=True)

class UpdatePriceCategoryRequestSerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=255, required=False, allow_null=True)
    unit_price_yen = serializers.IntegerField(min_value=0, required=False)
    effective_to = serializers.DateField(required=False, allow_null=True)
