from django.db import models


class ServiceModel(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=512)

    def __str__(self):
        return self.name
