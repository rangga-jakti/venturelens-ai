"""
VentureLens AI - Accounts Forms
Registration, Login, Profile forms with security validation.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Secure registration form."""

    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your full name',
            'class': 'auth-input',
            'autocomplete': 'name',
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'class': 'auth-input',
            'autocomplete': 'email',
        })
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Min. 8 characters',
            'class': 'auth-input',
            'autocomplete': 'new-password',
        })
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat password',
            'class': 'auth-input',
            'autocomplete': 'new-password',
        })
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '').strip()
        # Sanitize: only allow letters, spaces, hyphens
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", name):
            raise ValidationError('Name can only contain letters, spaces, and hyphens.')
        return name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.full_name = self.cleaned_data['full_name']
        # Auto-generate username from email
        base_username = self.cleaned_data['email'].split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Secure login form using email."""

    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'class': 'auth-input',
            'autocomplete': 'email',
            'autofocus': True,
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': 'auth-input',
            'autocomplete': 'current-password',
        })
    )


class ProfileForm(forms.ModelForm):
    """User profile update form."""

    class Meta:
        model = User
        fields = ('full_name', 'language')
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Your full name',
            }),
            'language': forms.Select(attrs={
                'class': 'auth-input',
            }),
        }
