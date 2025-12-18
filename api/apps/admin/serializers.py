from rest_framework import serializers  # type: ignore
from apps.users.models import User

class UpdateAdminUsersRequestSerializer(serializers.Serializer):
    """TBD in OpenAPI. We allow updating role and is_active."""
    role = serializers.ChoiceField(choices=[User.ROLE_ADMIN, User.ROLE_VIEWER], required=False)
    is_active = serializers.BooleanField(required=False)
