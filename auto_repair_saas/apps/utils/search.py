from django import forms


class SearchForm(forms.Form):
    input_attrs = {
        'class': 'form-control shadow-2',
        'style': 'background-color: #fff'
    }
    q = forms.CharField(
        widget=forms.TextInput(attrs=input_attrs), required=False
    )
