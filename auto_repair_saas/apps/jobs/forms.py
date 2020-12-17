from django import forms


class NewJobForm(forms.Form):
    CLIENT_CHOICES = [('', 'Select a client'), ('customer', 'Customer'), ]
    VEHICLE_CHOICES = [('', 'Select a vehicle'), ('vehicle', 'Vehicle'), ]
    MECHANIC_CHOICES = [('', 'Select a mechanic'), ('mechanic', 'Mechanic')]

    select_attrs = {'class': 'uk-select uk-form-width-medium'}
    input_attrs = {'class': 'uk-input uk-form-width-medium'}
    date_attrs = {'class': 'uk-input uk-form-width-medium', 'type': 'date'}

    client = forms.CharField(
        widget=forms.Select(choices=CLIENT_CHOICES, attrs=select_attrs)
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
