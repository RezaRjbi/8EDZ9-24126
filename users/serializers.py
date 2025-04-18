from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        exclude = ("groups", "user_permissions", "is_staff", "is_superuser", "is_active")
        read_only_fields = ("last_login", "date_joined")
