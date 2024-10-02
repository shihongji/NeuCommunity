from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        # Create a user instance for testing
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@northeastern.edu")

    def test_user_profile_creation(self):
        # Ensure that a UserProfile instance is created when a User is created
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_user_profile_string_representation(self):
        # Check the string representation of the UserProfile
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(user_profile), self.user.username)