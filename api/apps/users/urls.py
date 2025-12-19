from django.urls import path  # type: ignore
from .views import UsersListCreateView, UsersDetailView

urlpatterns = [
    path("users", UsersListCreateView.as_view(), name="users-list-create"),
    path("users/<uuid:userId>", UsersDetailView.as_view(), name="users-detail"),
]
