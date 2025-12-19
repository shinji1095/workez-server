from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("", include("apps.admin.urls")),
    path("", include("apps.devices.urls")),
    path("", include("apps.harvest.urls")),
    path("", include("apps.defects.urls")),
    path("", include("apps.prices.urls")),
    path("", include("apps.analytics.urls")),
]
