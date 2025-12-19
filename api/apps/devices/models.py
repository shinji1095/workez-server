import uuid
from django.db import models  # type: ignore

class Device(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_MAINTENANCE = "maintenance"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "active"),
        (STATUS_INACTIVE, "inactive"),
        (STATUS_MAINTENANCE, "maintenance"),
    ]

    id = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "devices"
        ordering = ["id"]

class BatteryStatus(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name="battery_status")
    percent = models.IntegerField()
    voltage_mv = models.IntegerField(null=True, blank=True)
    is_charging = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_battery_status"

class Alarm(models.Model):
    TYPE_BATTERY_LOW = "battery_low"
    TYPE_SENSOR_FAILURE = "sensor_failure"
    TYPE_NETWORK_ERROR = "network_error"
    TYPE_CHOICES = [
        (TYPE_BATTERY_LOW, "battery_low"),
        (TYPE_SENSOR_FAILURE, "sensor_failure"),
        (TYPE_NETWORK_ERROR, "network_error"),
    ]

    STATUS_OPEN = "open"
    STATUS_ACK = "acknowledged"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [
        (STATUS_OPEN, "open"),
        (STATUS_ACK, "acknowledged"),
        (STATUS_CLOSED, "closed"),
    ]

    SEVERITY_INFO = "info"
    SEVERITY_WARNING = "warning"
    SEVERITY_CRITICAL = "critical"
    SEVERITY_CHOICES = [
        (SEVERITY_INFO, "info"),
        (SEVERITY_WARNING, "warning"),
        (SEVERITY_CRITICAL, "critical"),
    ]

    alarm_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="alarms")
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_OPEN)
    severity = models.CharField(max_length=16, choices=SEVERITY_CHOICES, null=True, blank=True)
    occurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "device_alarms"
        ordering = ["-occurred_at"]
