from django import forms

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter a date b/w now and 4 weeks.')