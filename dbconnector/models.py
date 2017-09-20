from django.db import models


class ConnectionModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    db = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
