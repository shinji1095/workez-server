from __future__ import annotations

from rest_framework import serializers  # type: ignore

from apps.common.strict_fields import StrictDateTimeField, StrictPositiveIntField, StrictUUIDField

from .models import HarvestAggregateOverride, HarvestRecord, Rank, Size


class CreateHarvestAmountAddRequestSerializer(serializers.Serializer):
    event_id = StrictUUIDField()
    lot_name = serializers.CharField(max_length=64)
    size_id = serializers.SlugRelatedField(source="size", slug_field="size_id", queryset=Size.objects.all())
    rank_id = serializers.SlugRelatedField(source="rank", slug_field="rank_id", queryset=Rank.objects.all())
    count = StrictPositiveIntField()
    occurred_at = StrictDateTimeField()


class HarvestRecordSerializer(serializers.ModelSerializer):
    size_id = serializers.CharField(source="size.size_id")
    rank_id = serializers.CharField(source="rank.rank_id")

    class Meta:
        model = HarvestRecord
        fields = (
            "id",
            "event_id",
            "lot_name",
            "size_id",
            "rank_id",
            "count",
            "occurred_at",
            "created_at",
        )


class UpdateHarvestAmountOverrideRequestSerializer(serializers.Serializer):
    count = serializers.IntegerField()

    def validate_count(self, v):
        if isinstance(v, bool) or not isinstance(v, int):
            raise serializers.ValidationError("must be an integer")
        if v < 0:
            raise serializers.ValidationError("must be >= 0")
        return v


class HarvestAggregateOverrideSerializer(serializers.ModelSerializer):
    size_id = serializers.CharField(source="size.size_id")

    class Meta:
        model = HarvestAggregateOverride
        fields = (
            "id",
            "period_type",
            "size_id",
            "period",
            "total_count",
            "updated_at",
        )
