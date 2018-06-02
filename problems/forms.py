from django import forms

from common.compiler import SUPPORTED_COMPILERS


class SubmitForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea)
    language = forms.ChoiceField(choices=SUPPORTED_COMPILERS)
