from django import forms


class RegistrationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-input'}), max_length=100)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'uk-input'}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input'}), min_length=8)


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'uk-input'}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input'}), min_length=8)
