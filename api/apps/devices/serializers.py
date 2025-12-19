from rest_framework import serializers  # type: ignore
from .models import Device, BatteryStatus, Alarm

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "name", "status", "created_at", "updated_at"]

class CreateDeviceRequestSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=255)
    status = serializers.ChoiceField(choices=[c[0] for c in Device.STATUS_CHOICES], required=False)

class BatteryUpdateRequestSerializer(serializers.Serializer):
    percent = serializers.IntegerField(min_value=0, max_value=100)
    voltage_mv = serializers.IntegerField(required=False, allow_null=True)
    is_charging = serializers.BooleanField()

class BatteryLatestSerializer(serializers.Serializer):
    device_id = serializers.CharField()
    percent = serializers.IntegerField()
    voltage_mv = serializers.IntegerField(allow_null=True, required=False)
    is_charging = serializers.BooleanField()
    updated_at = serializers.DateTimeField()

class AlarmCreateRequestSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=[c[0] for c in Alarm.TYPE_CHOICES])
    message = serializers.CharField()
    severity = serializers.ChoiceField(choices=[c[0] for c in Alarm.SEVERITY_CHOICES], required=False, allow_null=True)
    occurred_at = serializers.DateTimeField(required=False)

class AlarmItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ["alarm_id", "type", "message", "status", "occurred_at"]

class AlarmStatusSerializer(serializers.Serializer):
    device_id = serializers.CharField()
    has_active_alarm = serializers.BooleanField()
    severity = serializers.CharField(allow_null=True, required=False)
    last_alarm_at = serializers.DateTimeField(allow_null=True, required=False)
    active_alarms = AlarmItemSerializer(many=True, required=False, allow_null=True)
