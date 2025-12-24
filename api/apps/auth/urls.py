from django.urls import path  # type: ignore

from .views import AuthTokenView

urlpatterns = [
    path("auth/token", AuthTokenView.as_view(), name="auth-token"),
]
