from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.Form):
    input_attrs = {'class': 'uk-input long-input'}
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
    input_attrs = {'class': 'uk-input long-input'}
    username = forms.EmailField(widget=forms.EmailInput(
        attrs=input_attrs),
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs=input_attrs), min_length=8
    )
