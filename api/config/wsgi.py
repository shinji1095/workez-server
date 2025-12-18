import os
from django.core.wsgi import get_wsgi_application  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.local"))

application = get_wsgi_application()
