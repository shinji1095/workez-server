from django.apps import AppConfig  # type: ignore

class AdminApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.admin"
    label = "admin_api"
