from django.db import models


class JobModel(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    file = models.CharField(max_length=512)
    schema = models.CharField(max_length=20480)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    finalized = models.BooleanField(default=False)
