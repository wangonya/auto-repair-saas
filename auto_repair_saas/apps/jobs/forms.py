from django import forms

from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.staff.models import Staff
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

    select_attrs = {'class': 'form-control'}
    input_attrs = {'class': 'form-control'}
    date_attrs = {
        'class': 'form-control',
        'type': 'date',
        'placeholder': 'Select date'
    }
    job_status_choices = (('pending', 'Pending (Estimate)'),
                          ('confirmed', 'Confirmed (Estimate)'),
                          ('in_progress', 'In progress'),
                          ('done', 'Done'))
    payment_method_choices = (('cash', 'Cash'),
                              ('card', 'Card'),
                              ('mpesa', 'M-Pesa'))

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
    assigned = forms.ModelChoiceField(
        queryset=Staff.objects.all(),
        widget=forms.Select(attrs=select_attrs), required=False
    )
    charged = forms.CharField(widget=forms.NumberInput(
        attrs={**input_attrs, **{'value': 0}}), required=False
    )
    status = forms.ChoiceField(
        choices=job_status_choices,
        widget=forms.Select(attrs=select_attrs)
    )
    payment_method = forms.ChoiceField(
        choices=payment_method_choices,
        widget=forms.Select(attrs=select_attrs)
    )


class SearchJobsForm(forms.Form):
    input_attrs = {
        'class': 'form-control shadow-2',
        'style': 'background-color: #fff'
    }
    q = forms.CharField(
        widget=forms.TextInput(attrs=input_attrs), required=False
    )
