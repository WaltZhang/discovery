from django.forms import ModelForm, CharField, Textarea, ClearableFileInput, FileField

from fileconnector.models import FileModel


class FileForm(ModelForm):
    file = FileField(widget=ClearableFileInput(
        attrs={
            'class': 'form-control'
        }
    ))
    description = CharField(widget=Textarea(
        attrs={
            'class': 'form-control'
        }
    ))

    class Meta:
        model = FileModel
        fields = ["file", "description"]
