from django.db import models


class InventoryModel(models.Model):
    name = models.CharField(max_length=256)
    schema = models.TextField()
    sample = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
