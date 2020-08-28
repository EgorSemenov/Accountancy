from django import forms
from .models import File


class FileUploadForm(forms.ModelForm):  # класс, который отвечает за форму, для загрузки файла, наследуется от django класса
    file = forms.FileField(label='', )
    # TODO: file name duplicate validation

    class Meta:
        model = File
        exclude = ('id', 'name')
