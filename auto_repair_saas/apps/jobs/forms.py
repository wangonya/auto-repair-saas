from django import forms

from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.vehicles.models import Vehicle


class NewJobForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.none()
        if 'client' in self.data:
            try:
                owner_id = int(self.data.get('client'))
                self.fields['vehicle'].queryset = Vehicle.objects.filter(
                    owner_id=owner_id
                )
            except (ValueError, TypeError):
                pass  # invalid input; fallback to empty Vehicle queryset

    MECHANIC_CHOICES = [('', 'Select a mechanic'), ]

    select_attrs = {'class': 'uk-select uk-form-width-medium'}
    input_attrs = {'class': 'uk-input uk-form-width-medium'}
    date_attrs = {'class': 'uk-input uk-form-width-medium', 'type': 'date'}

    client = forms.ModelChoiceField(
        queryset=Contact.objects.filter(contact_type='client'),
        widget=forms.Select(attrs=select_attrs)
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.none(),
        widget=forms.Select(attrs=select_attrs)
    )
    due_start_date = forms.DateField(
        widget=forms.DateInput(attrs=date_attrs), required=False
    )
    due_end_date = forms.DateField(
        widget=forms.DateInput(attrs=date_attrs), required=False
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'uk-textarea', 'rows': '3'}),
        required=False
    )
    assigned = forms.CharField(
        widget=forms.Select(attrs=select_attrs, choices=MECHANIC_CHOICES, ),
        required=False
    )
    charged = forms.CharField(widget=forms.NumberInput(
        attrs={**input_attrs, **{'value': 0}}), required=False
    )
