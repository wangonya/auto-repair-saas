from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, \
    SetPasswordForm


class RegistrationForm(forms.Form):
    input_attrs = {'class': 'form-control'}
    name = forms.CharField(widget=forms.TextInput(
        attrs=input_attrs), max_length=100
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs=input_attrs),
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs=input_attrs), min_length=8
    )


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
