from django.forms import ModelForm

from fileconnector.models import FileModel


class FileForm(ModelForm):
    class Meta:
        model = FileModel
        fields = ["file", "description"]
