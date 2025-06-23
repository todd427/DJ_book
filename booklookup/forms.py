
from django import forms

class AuthorSearchForm(forms.Form):
    author = forms.CharField(label='Author Name', max_length=100)
