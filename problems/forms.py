from django import forms

from common.compiler import SUPPORTED_LANGUAGE


class SubmitForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea)
    language = forms.ChoiceField(choices=SUPPORTED_LANGUAGE)
