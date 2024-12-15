from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import Profile
from django.urls import reverse


class TestUserRegisterView(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.token_url = reverse("get_token")
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
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
        self.update_data = {"age": 30, "weight": 72}

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["Message"], "User created successfully!!!")
        self.assertTrue(Profile.objects.filter(user__username="testuser").exists())

    def test_user_registration_missing_profile(self):
        incomplete_data = self.user_data.copy()
        incomplete_data.pop("profile")
        response = self.client.post(self.register_url, incomplete_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update_authenticated_user(self):
        self.client.post(self.register_url, self.user_data, format="json")
        token_response = self.client.post(
            self.token_url,
            {"username": "testuser", "password": "testpassword123"},
            format="json",
        )
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.put(self.register_url, self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Profile Updated Successfully")
        profile = Profile.objects.get(user__username="testuser")
        self.assertEqual(profile.age, 30)
        self.assertEqual(float(profile.weight), 72.0)

    def test_profile_update_unauthenticated_user(self):
        response = self.client.put(self.register_url, self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_user_missing_fields(self):
        invalid_data = self.user_data.copy()
        invalid_data.pop("username")
        response = self.client.post(self.register_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
