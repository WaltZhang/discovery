from django.db import models


class ConnectionModel(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    user = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    connection = models.CharField(max_length=200)
