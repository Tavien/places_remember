from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for new user class
    """
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "photo")
