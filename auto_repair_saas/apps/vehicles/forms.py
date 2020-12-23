from django import forms

from auto_repair_saas.apps.contacts.models import Contact


class NewVehicleForm(forms.Form):
    select_attrs = {'class': 'form-control'}
    input_attrs = {'class': 'form-control'}

    number_plate = forms.CharField(widget=forms.TextInput(attrs=input_attrs))
    owner = forms.ModelChoiceField(
        queryset=Contact.objects.filter(contact_type='client'),
        widget=forms.Select(attrs=select_attrs)
    )
