from rest_framework import serializers  # type: ignore
from .models import PriceRecord

class PriceRecordSerializer(serializers.ModelSerializer):
    size_id = serializers.CharField(source="size.size_id")
    rank_id = serializers.CharField(source="rank.rank_id")

    class Meta:
        model = PriceRecord
        fields = ["size_id", "rank_id", "year", "month", "unit_price_yen", "updated_at"]

class UpsertPricesSizeRankRequestSerializer(serializers.Serializer):
    year = serializers.IntegerField(min_value=2000, max_value=2100)
    month = serializers.IntegerField(min_value=1, max_value=12)
    unit_price_yen = serializers.IntegerField(min_value=0)
