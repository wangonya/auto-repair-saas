from django import forms

from auto_repair_saas.apps.contacts.models import Contact


class NewVehicleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        owners = Contact.objects.filter(contact_type='client')
        self.fields['owner'].queryset = owners

    select_attrs = {'class': 'form-control'}
    input_attrs = {'class': 'form-control'}

    number_plate = forms.CharField(widget=forms.TextInput(attrs=input_attrs))
    owner = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs=select_attrs)
    )
