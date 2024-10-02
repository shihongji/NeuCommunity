from django.test import TestCase
from users.forms import CustomUserCreationForm

class CustomUserCreationFormTest(TestCase):
    def test_custom_user_creation_form_valid(self):
        # Test valid form data
        form_data = {
            "username": "newuser",
            "email": "newuser@northeastern.edu",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_invalid_email(self):
        # Test invalid email domain
        form_data = {
            "username": "newuser",
            "email": "newuser@gmail.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Email must be from the 'northeastern.edu' domain.", form.errors["email"])