from django import forms
from .models import *



class FilterOrderForm(forms.Form):
    ordering = [('name', 'Jmena A-Z'), ('-name', 'Jmena Z-A'), ('source', 'Zdroj A-Z'), ('-source', 'Zdroj Z-A')]
    ordering = forms.ChoiceField(choices=ordering, label="Radit podle:")
    filter_Disabled = forms.BooleanField(label="Filtrovat Ativovane", required=False)
    filter_Featured = forms.BooleanField(label="Filtrovat Hity",required=False)

    class Meta:
        fields = ('ordering', 'filter_Disabled', 'filter_Featured')