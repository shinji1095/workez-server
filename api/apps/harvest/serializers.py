from __future__ import annotations

from rest_framework import serializers  # type: ignore

from apps.common.strict_fields import StrictDateTimeField, StrictPositiveIntField, StrictUUIDField

from .models import HarvestAggregateOverride, HarvestRecord


class CreateHarvestAmountAddRequestSerializer(serializers.Serializer):
    event_id = StrictUUIDField()
    device_id = serializers.CharField()
    category_id = serializers.CharField()
    count = StrictPositiveIntField()
    occurred_at = StrictDateTimeField()


class HarvestRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestRecord
        fields = (
            "id",
            "event_id",
            "device_id",
            "category_id",
            "category_name",
            "count",
            "occurred_at",
            "created_at",
        )


class UpdateHarvestAmountOverrideRequestSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()

    def validate_total_count(self, v):
        if isinstance(v, bool) or not isinstance(v, int):
            raise serializers.ValidationError("must be an integer")
        if v < 0:
            raise serializers.ValidationError("must be >= 0")
        return v


class HarvestAggregateOverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestAggregateOverride
        fields = (
            "id",
            "period_type",
            "category_id",
            "period",
            "total_count",
            "created_at",
        )
