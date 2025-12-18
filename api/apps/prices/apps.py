from django.apps import AppConfig  # type: ignore

class PricesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.prices"
    label = "prices_api"
