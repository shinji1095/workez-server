import uuid
from django.db import models  # type: ignore

class User(models.Model):
    """Application user (separate from Django auth user)."""
    ROLE_ADMIN = "admin"
    ROLE_VIEWER = "viewer"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "admin"),
        (ROLE_VIEWER, "viewer"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_VIEWER)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "app_users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.email} ({self.role})"
