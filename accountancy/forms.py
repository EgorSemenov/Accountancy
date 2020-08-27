from django import forms
from django.forms import ClearableFileInput

from .models import File


class FileUploadForm(forms.ModelForm):
    file = forms.FileField(label='', )
    class Meta:
        model = File
        exclude = ('id', 'name')
