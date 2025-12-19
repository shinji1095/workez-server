from django.apps import AppConfig  # type: ignore

class DefectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.defects"
    label = "defects_api"
