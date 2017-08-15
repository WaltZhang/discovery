from django.contrib import admin

from django.contrib.admin import ModelAdmin

from fileconnector.models import FileModel, MetadataModel
from sparkjob.models import JobModel


class MetadataModelAdmin(ModelAdmin):
    list_display = ['file', 'description', 'metadata', 'timestamp', 'updated']
    class Meta:
        model = MetadataModel


class FileConnectorModelAdmin(ModelAdmin):
    list_display = ['file', 'description']
    class Meta:
        model = FileModel


class JobModelAdmin(ModelAdmin):
    list_display = ['name', 'description', 'schema', 'timestamp', 'updated']
    class Meta:
        model = JobModel


admin.site.register(FileModel, FileConnectorModelAdmin)
admin.site.register(MetadataModel, MetadataModelAdmin)
admin.site.register(JobModel, JobModelAdmin)
