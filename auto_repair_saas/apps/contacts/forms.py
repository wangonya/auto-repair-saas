from django import forms


class NewContactForm(forms.Form):
    CONTACT_TYPE_CHOICES = (
        ('client', 'Client'), ('supplier', 'Supplier'),
    )

    select_attrs = {'class': 'form-control'}
    input_attrs = {'class': 'form-control'}

    contact_type = forms.CharField(
        widget=forms.Select(choices=CONTACT_TYPE_CHOICES, attrs=select_attrs)
    )
    name = forms.CharField(widget=forms.TextInput(attrs=input_attrs))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            **input_attrs,
            **{
                'type': 'tel',
                'title': "07xxxxxxxx",
                'data-mdb-toggle': "tooltip"
            }
        }), required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=input_attrs), required=False
    )
