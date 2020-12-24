from django import forms

from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.vehicles.models import Vehicle


class NewJobForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'client' in self.data:
            try:
                owner_id = int(self.data.get('client'))
                self.fields['vehicle'].queryset = Contact.objects.get(
                    owner_id).vehicle_set.all()
            except (ValueError, TypeError):
                pass  # invalid input; fallback to empty Vehicle queryset

    MECHANIC_CHOICES = [('', 'Select a mechanic'), ]

    select_attrs = {'class': 'form-control'}
    input_attrs = {'class': 'form-control'}
    date_attrs = {
        'class': 'form-control',
        'type': 'date',
        'placeholder': 'Select date'
    }

    client = forms.ModelChoiceField(
        queryset=Contact.objects.filter(contact_type='client'),
        widget=forms.Select(attrs=select_attrs)
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        widget=forms.Select(attrs=select_attrs)
    )
    due_start_date = forms.DateField(
        widget=forms.DateInput(attrs=date_attrs), required=False
    )
    due_end_date = forms.DateField(
        widget=forms.DateInput(attrs=date_attrs), required=False
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={**input_attrs, **{'rows': 3}}), required=False
    )
    assigned = forms.CharField(
        widget=forms.Select(attrs=select_attrs, choices=MECHANIC_CHOICES, ),
        required=False
    )
    charged = forms.CharField(widget=forms.NumberInput(
        attrs={**input_attrs, **{'value': 0}}), required=False
    )
