__author__ = 'naman'

from django import forms

class DocumentForm(forms.Form):
    docfile=forms.FileField(label='Select a file')
    status=forms.CharField(max_length=100)

class DocForm(forms.Form):
    name=forms.CharField(max_length=100)