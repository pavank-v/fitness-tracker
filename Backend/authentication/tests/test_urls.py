from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import UserRegisterView
from django.test import SimpleTestCase


class TestAuthenticationURLs(SimpleTestCase):
    def test_user_register_url(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func.view_class, UserRegisterView)

    def test_get_token_url(self):
        url = reverse("get_token")
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        url = reverse("refresh")
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_api_auth_url(self):
        url = reverse("rest_framework:login")
        self.assertEqual(resolve(url).namespace, "rest_framework")
