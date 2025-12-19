from django.apps import AppConfig  # type: ignore

class DevicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.devices"
    label = "devices_api"
