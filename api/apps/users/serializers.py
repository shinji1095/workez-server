from rest_framework import serializers  # type: ignore
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "role", "is_active", "created_at", "updated_at"]

class CreateUsersRequestSerializer(serializers.Serializer):
    """TBD in OpenAPI. We accept a practical subset and keep others flexible."""
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(choices=[User.ROLE_ADMIN, User.ROLE_VIEWER], required=False)
    is_active = serializers.BooleanField(required=False)

class PartialUpdateUsersRequestSerializer(serializers.Serializer):
    """TBD in OpenAPI."""
    email = serializers.EmailField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    is_active = serializers.BooleanField(required=False)

