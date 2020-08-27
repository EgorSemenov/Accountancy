from django import forms
from django.forms import ClearableFileInput

from .models import File


class FileUploadForm(forms.ModelForm):  # класс, который отвечает за форму, для загрузки файла, наследуется от django класса
    file = forms.FileField(label='', )

    class Meta:
        model = File  # указывает модель связанную с данной формой
        exclude = ('id',
                   'name')  # удаляет заполнение полей, соответствующих полям в модели и соответсвенно в бд, с такими названиями
