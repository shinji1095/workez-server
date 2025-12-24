from rest_framework import serializers  # type: ignore


class CreateAuthTokenRequestSerializer(serializers.Serializer):
    sub = serializers.CharField(min_length=1, max_length=128)
