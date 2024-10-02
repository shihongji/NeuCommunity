from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile


# Custom validator to ensure email is from the Northeastern domain
def validate_northeastern_email(email: str) -> None:
    domain = "northeastern.edu"
    if not email.endswith(f"@{domain}"):
        raise ValidationError(f"Email must be from the '{domain}' domain.")


class CustomUserCreationForm(UserCreationForm):
    """
    Form to create a new user account with a Northeastern email address.
    """
    email = forms.EmailField(
        max_length=255,
        required=True,
        help_text="Restrict to a Northeastern.edu address.",
        validators=[validate_northeastern_email],
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self) -> str:
        """
        Validate that the username is unique.
        """
        username: str = self.cleaned_data.get("username", "").strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        """
        Validate that the email is unique.
        """
        email: str = self.cleaned_data.get("email", "").strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email


class UserProfileForm(forms.ModelForm):
    """
    Form for creating and updating a user's profile.
    """
    class Meta:
        model = UserProfile
        fields = [
            "description",
            "blog_site",
            "github_address",
            "linkedin_address",
            "twitter_address",
            "instagram_address",
        ]
        labels = {
            "description": "Description",
            "blog_site": "Blog URL",
            "github_address": "GitHub URL",
            "linkedin_address": "LinkedIn URL",
            "twitter_address": "Twitter URL",
            "instagram_address": "Instagram URL",
        }
        # Add placeholders to form fields, textareas to allow for multiple lines
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Tell us about yourself..."}),
            "blog_site": forms.URLInput(attrs={"placeholder": "https://yourblog.com"}),
            "github_address": forms.URLInput(attrs={"placeholder": "https://github.com/yourusername"}),
            "linkedin_address": forms.URLInput(attrs={"placeholder": "https://linkedin.com/in/yourusername"}),
            "twitter_address": forms.URLInput(attrs={"placeholder": "https://twitter.com/yourusername"}),
            "instagram_address": forms.URLInput(attrs={"placeholder": "https://instagram.com/yourusername"}),
        }
