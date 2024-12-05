from rest_framework import serializers
from django.contrib.auth.models import User

from authentication.models import Profile
# Serializer for Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


# Serializer for User details
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "profile",
        ]
        extra_kwargs = {
            "password": {"write_only": True},  # Make password write-only
        }

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user

