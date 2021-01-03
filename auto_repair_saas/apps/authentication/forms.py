from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, \
    SetPasswordForm
from django.core.exceptions import ValidationError

from auto_repair_saas.apps.authentication.models import User


class RegistrationForm(forms.Form):
    error_messages = {
        'password_mismatch': 'The two password fields didn’t match.',
    }
    input_attrs = {'class': 'form-control'}
    name = forms.CharField(widget=forms.TextInput(
        attrs=input_attrs), max_length=100
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs=input_attrs),
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs=input_attrs), min_length=8
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs=input_attrs), min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")
        username = cleaned_data.get("name")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(
            password2, User(email=email, username=username)
        )
        return cleaned_data


class LoginForm(AuthenticationForm):
    input_attrs = {'class': 'form-control'}
    username = forms.EmailField(widget=forms.EmailInput(
        attrs=input_attrs),
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs=input_attrs), min_length=8
    )


class PasswordResetRequestForm(PasswordResetForm):
    input_attrs = {'class': 'form-control', 'autocomplete': 'email'}
    email = forms.EmailField(widget=forms.EmailInput(
        attrs=input_attrs), max_length=254,
    )


class PasswordResetConfirmForm(SetPasswordForm):
    input_attrs = {'class': 'form-control', 'autocomplete': 'new-password'}
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=input_attrs),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs=input_attrs),
    )
