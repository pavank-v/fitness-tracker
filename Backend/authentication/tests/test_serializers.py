from django.test import TestCase
from django.contrib.auth.models import User
from authentication.models import Profile
from authentication.serializers import UserSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "first_name": "Test",
            "last_name": "User",
            "profile": {
                "age": 25,
                "gender": "M", 
                "weight": 70.5,
                "height": 175.0,
                "current_level": "Beginner",  
                "goal": "Maintain", 
            },
        }

    def test_valid_user_data(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.profile.age, 25)
        self.assertEqual(user.profile.gender, "M")
        self.assertEqual(user.profile.weight, 70.5)

    def test_missing_required_field(self):
        invalid_data = self.user_data.copy()
        invalid_data.pop("username")  
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_password_write_only(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertNotIn("password", UserSerializer(user).data)

    def test_serialized_output(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
        )
        Profile.objects.create(
            user=user,
            age=25,
            gender="M",
            weight=70.5,
            height=175.0,
            current_level="Beginner",
            goal="Maintain",
        )
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data["username"], "testuser")
        self.assertEqual(serializer.data["profile"]["age"], 25)
        self.assertEqual(serializer.data["profile"]["gender"], "M")
