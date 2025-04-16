from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.models import Profile

# Serializer for Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}  # Prevent user ID modification

# Serializer for User details
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)  # Profile is optional

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
            "password": {"write_only": True},  
        }

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        password = validated_data.pop("password", None)

        user = User.objects.create_user(**validated_data) 
        if password:
            user.set_password(password)
        user.save()

        if profile_data:
            Profile.objects.create(user=user, **profile_data)

        return user

    def update(self, instance, validated_data):
        """
        Update user and profile data.
        """
        profile_data = validated_data.pop("profile", None)
        
        # Update user fields
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)  
            else:
                setattr(instance, attr, value)
        instance.save()

        if profile_data:
            profile, _ = Profile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance
