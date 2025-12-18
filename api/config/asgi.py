import os
from django.core.asgi import get_asgi_application  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.local"))

application = get_asgi_application()
