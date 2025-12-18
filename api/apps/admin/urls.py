from django.urls import path  # type: ignore
from .views import AdminUsersUpdateView

urlpatterns = [
    path("admin/users/<uuid:userId>", AdminUsersUpdateView.as_view(), name="admin-users-update"),
]
