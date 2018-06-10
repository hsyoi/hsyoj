from django import forms

from common.compiler import SUPPORTED_COMPILERS


class SubmitForm(forms.Form):
    source_code = forms.CharField(widget=forms.Textarea)
    compiler = forms.ChoiceField(choices=SUPPORTED_COMPILERS)
