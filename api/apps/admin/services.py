from typing import Dict, Any
from django.db import transaction  # type: ignore
from apps.users.models import User
from apps.users import services as user_services

@transaction.atomic
def update_admin_user(user_id: str, data: Dict[str, Any]) -> User:
    user = User.objects.get(pk=user_id)
    if "role" in data:
        user.role = data["role"]
    if "is_active" in data:
        user.is_active = data["is_active"]
    user.save(update_fields=["role", "is_active", "updated_at"])
    return user
