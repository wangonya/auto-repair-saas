from datetime import date

from django import forms

from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.staff.models import Staff
from auto_repair_saas.apps.vehicles.models import Vehicle


class NewJobForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clients = Contact.objects.filter(contact_type='client')
        staff = Staff.objects.all()
        vehicles = Vehicle.objects.all()
        self.fields['client'].queryset = clients
        self.fields['assigned'].queryset = staff
        self.fields['vehicle'].queryset = vehicles
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
        'placeholder': 'dd/mm/yyyy'
    }
    job_status_choices = (('pending', 'Pending (Estimate)'),
                          ('confirmed', 'Confirmed (Estimate)'),
                          ('in_progress', 'In progress'),
                          ('done', 'Done'))
    payment_method_choices = (('cash', 'Cash'),
                              ('card', 'Card'),
                              ('mpesa', 'M-Pesa'))

    client = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs=select_attrs)
    )
    vehicle = forms.ModelChoiceField(
        queryset=None,
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
        required=False,
        queryset=None,
        widget=forms.Select(attrs=select_attrs)
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

    def clean(self):
        start_date = self.cleaned_data.get('due_start_date')
        end_date = self.cleaned_data.get('due_end_date')
        if not (start_date and end_date):
            return self.cleaned_data
        if start_date > end_date:
            raise forms.ValidationError(
                'Due start date can not be later than due end date.'
            )


class RegisterPaymentForm(forms.Form):
    paid = forms.BooleanField(initial=True, widget=forms.HiddenInput())
    payment_registered_on = forms.DateField(
        initial=date.today(), widget=forms.HiddenInput()
    )
