from django import forms

from auto_repair_saas.apps.contacts.models import Contact


class NewJobForm(forms.Form):
    VEHICLE_CHOICES = [('', 'Select a vehicle'), ]
    MECHANIC_CHOICES = [('', 'Select a mechanic'), ]

    select_attrs = {'class': 'uk-select uk-form-width-medium'}
    input_attrs = {'class': 'uk-input uk-form-width-medium'}
    date_attrs = {'class': 'uk-input uk-form-width-medium', 'type': 'date'}

    client = forms.ModelChoiceField(
        queryset=Contact.objects.filter(contact_type='client'),
        widget=forms.Select(attrs=select_attrs)
    )
    vehicle = forms.CharField(
        widget=forms.Select(choices=VEHICLE_CHOICES, attrs=select_attrs)
    )
    due_start_date = forms.DateField(
        widget=forms.DateInput(attrs=date_attrs), required=False
    )
    due_end_date = forms.DateField(
        widget=forms.DateInput(attrs=date_attrs), required=False
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'uk-textarea', 'rows': '3', 'cols': '61'}),
        required=False
    )
    assigned = forms.CharField(
        widget=forms.Select(attrs=select_attrs, choices=MECHANIC_CHOICES, ),
        required=False
    )
    charged = forms.CharField(widget=forms.TextInput(
        attrs={**input_attrs, **{'type': 'number'}}), required=False
    )
