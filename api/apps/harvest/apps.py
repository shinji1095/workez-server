from django.apps import AppConfig  # type: ignore

class HarvestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.harvest"
    label = "harvest_api"
