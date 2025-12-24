from django.apps import AppConfig  # type: ignore


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.auth"
    label = "auth_api"
