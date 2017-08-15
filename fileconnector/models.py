from django.db import models


class FileModel(models.Model):
    file = models.FileField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.description


class MetadataModel(models.Model):
    file = models.FileField(null=True, blank=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    metadata = models.CharField(max_length=4096)

    def __str__(self):
        return self.description
