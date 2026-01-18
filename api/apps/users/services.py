from __future__ import annotations
from typing import Dict, Any, Tuple
from django.db import transaction  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from .models import User

@transaction.atomic
def create_user(data: Dict[str, Any]) -> User:
    user = User.objects.create(
        email=data["email"],
        name=data["name"],
        role=data.get("role", User.ROLE_USER),
    )
    return user

def list_users(page: int, page_size: int) -> Tuple[list[User], int]:
    qs = User.objects.all().order_by("-created_at")
    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    return list(qs[start:end]), total

@transaction.atomic
def partial_update_user(user_id: str, data: Dict[str, Any]) -> User:
    user = get_object_or_404(User, pk=user_id)
    for k in ["email", "name"]:
        if k in data:
            setattr(user, k, data[k])
    user.save(update_fields=["email", "name", "updated_at"])
    return user

@transaction.atomic
def update_user_role(user_id: str, role: str) -> User:
    user = get_object_or_404(User, pk=user_id)
    user.role = role
    user.save(update_fields=["role", "updated_at"])
    return user

@transaction.atomic
def delete_user(user_id: str) -> None:
    user = get_object_or_404(User, pk=user_id)
    user.delete()
