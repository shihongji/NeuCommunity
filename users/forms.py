from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_northeastern_email(email):
    domain = "northeastern.edu"
    if not email.endswith(f"@{domain}"):
        raise ValidationError(f"Email must be from the '{domain}' domain.")


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text="Restrict to a Northeastern.edu address.",
                             validators=[validate_northeastern_email])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email
