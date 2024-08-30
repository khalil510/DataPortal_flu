
from django import forms

class DatabaseForm(forms.Form):
    database = forms.CharField(label='Database', max_length=100)

class TableForm(forms.Form):
    table = forms.CharField(label='Table', max_length=100)



