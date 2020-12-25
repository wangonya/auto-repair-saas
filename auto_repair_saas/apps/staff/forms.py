from django import forms


class NewStaffForm(forms.Form):
    select_attrs = {'class': 'form-control'}
    input_attrs = {'class': 'form-control'}

    name = forms.CharField(widget=forms.TextInput(attrs=input_attrs))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=input_attrs), required=False
    )
