from __future__ import annotations
from typing import Any, Dict, Tuple, Optional
from django.db import transaction  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from django.utils import timezone  # type: ignore

from .models import Device, BatteryStatus, Alarm

@transaction.atomic
def create_device(data: Dict[str, Any]) -> Device:
    device = Device.objects.create(
        id=data["id"],
        name=data["name"],
        status=data.get("status", Device.STATUS_ACTIVE),
    )
    return device

def list_devices(page: int, page_size: int) -> Tuple[list[Device], int]:
    qs = Device.objects.all().order_by("id")
    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    return list(qs[start:end]), total

@transaction.atomic
def delete_device(device_id: str) -> None:
    device = get_object_or_404(Device, pk=device_id)
    device.delete()

@transaction.atomic
def upsert_battery(device_id: str, data: Dict[str, Any]) -> BatteryStatus:
    device = get_object_or_404(Device, pk=device_id)
    obj, _ = BatteryStatus.objects.update_or_create(
        device=device,
        defaults={
            "percent": data["percent"],
            "voltage_mv": data.get("voltage_mv"),
            "is_charging": data["is_charging"],
        },
    )
    return obj

def get_battery_latest(device_id: str) -> Optional[BatteryStatus]:
    device = get_object_or_404(Device, pk=device_id)
    try:
        return device.battery_status
    except BatteryStatus.DoesNotExist:
        return None

@transaction.atomic
def create_alarm(device_id: str, data: Dict[str, Any]) -> Alarm:
    device = get_object_or_404(Device, pk=device_id)
    occurred_at = data.get("occurred_at") or timezone.now()
    alarm = Alarm.objects.create(
        device=device,
        type=data["type"],
        message=data["message"],
        severity=data.get("severity"),
        occurred_at=occurred_at,
        status=Alarm.STATUS_OPEN,
    )
    return alarm

def get_alarm_status(device_id: str) -> Dict[str, Any]:
    device = get_object_or_404(Device, pk=device_id)
    active_qs = device.alarms.filter(status=Alarm.STATUS_OPEN).order_by("-occurred_at")
    has_active = active_qs.exists()
    last_alarm = device.alarms.order_by("-occurred_at").first()
    severity = None
    if has_active:
        sev_map = {Alarm.SEVERITY_INFO: 1, Alarm.SEVERITY_WARNING: 2, Alarm.SEVERITY_CRITICAL: 3}
        # pick max severity among open alarms, if any
        max_sev = 0
        for a in active_qs[:20]:
            v = sev_map.get(a.severity or "", 0)
            if v > max_sev:
                max_sev = v
                severity = a.severity
    return {
        "device_id": device.id,
        "has_active_alarm": has_active,
        "severity": severity,
        "last_alarm_at": last_alarm.occurred_at if last_alarm else None,
        "active_alarms": list(active_qs[:20]),
    }

def list_alarm_items(device_id: str, page: int, page_size: int) -> Tuple[list[Alarm], int]:
    device = get_object_or_404(Device, pk=device_id)
    qs = device.alarms.all().order_by("-occurred_at")
    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    return list(qs[start:end]), total
