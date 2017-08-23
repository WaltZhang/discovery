from django.db import models


class FileModel(models.Model):
    file = models.FileField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.description
