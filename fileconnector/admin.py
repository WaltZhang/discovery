from django.contrib import admin

from django.contrib.admin import ModelAdmin

from fileconnector.models import FileModel
from sparkjob.models import CsvModel


class FileConnectorModelAdmin(ModelAdmin):
    list_display = ['file', 'description']
    class Meta:
        model = FileModel


class JobModelAdmin(ModelAdmin):
    list_display = ['name', 'description', 'schema', 'timestamp', 'updated']
    class Meta:
        model = CsvModel


admin.site.register(FileModel, FileConnectorModelAdmin)
admin.site.register(CsvModel, JobModelAdmin)
