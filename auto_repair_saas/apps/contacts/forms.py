from django import forms


class NewContactForm(forms.Form):
    CONTACT_TYPE_CHOICES = (
        ('client', 'Client'), ('supplier', 'Supplier'),
    )

    select_attrs = {'class': 'uk-select uk-form-width-medium'}
    input_attrs = {'class': 'uk-input uk-form-width-medium'}

    contact_type = forms.CharField(
        widget=forms.Select(choices=CONTACT_TYPE_CHOICES, attrs=select_attrs)
    )
    name = forms.CharField(widget=forms.TextInput(attrs=input_attrs))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            **input_attrs,
            **{'type': 'number', 'uk-tooltip': "07xxxxxxxx"}
        }), required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=input_attrs), required=False
    )
