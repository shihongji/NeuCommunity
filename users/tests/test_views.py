from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@northeastern.edu")
        self.client.login(username="testuser", password="testpass")

    def test_profile_view(self):
        # Test that the profile view returns a 200 response for the logged-in user
        response = self.client.get(reverse("users:profile", args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_login_view(self):
        # Test that the login view returns a 200 response
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")