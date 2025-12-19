from django.urls import path  # type: ignore
from .views import (
    DevicesListCreateView,
    DevicesDeleteView,
    DevicesBatteryView,
    DevicesAlermView,
    DevicesAlermDetailView,
)

urlpatterns = [
    path("devices", DevicesListCreateView.as_view(), name="devices-list-create"),
    path("devices/<str:deviceId>", DevicesDeleteView.as_view(), name="devices-delete"),
    path("devices/<str:deviceId>/battery", DevicesBatteryView.as_view(), name="devices-battery"),
    path("devices/<str:deviceId>/alerm", DevicesAlermView.as_view(), name="devices-alerm"),
    path("devices/<str:deviceId>/alerm/detail", DevicesAlermDetailView.as_view(), name="devices-alerm-detail"),
]
